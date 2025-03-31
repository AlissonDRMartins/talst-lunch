from dataclasses import dataclass
import boto3
from sqlalchemy import create_engine, text
from sqlalchemy.engine import URL


@dataclass
class DSQLConnection:
    secret_key: str
    access_key: str
    region: str
    hostname: str
    database: str
    username: str

    def __post_init__(self):
        self.session = boto3.Session(
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            region_name=self.region,
        )
        # DSQL is the correct service name
        self.dsql_client = self.session.client("dsql", region_name=self.region)

    def get_db_auth_token(self):
        # Use the correct method for DSQL
        return self.dsql_client.generate_db_connect_admin_auth_token(
            self.hostname, self.region
        )

    def create_dsql_engine(self):
        # Create proper SQLAlchemy URL
        url = URL.create(
            "postgresql",
            username=self.username,
            password=self.get_db_auth_token(),
            host=self.hostname,
            database=self.database,
        )

        # Create engine with SSL required
        engine = create_engine(url, connect_args={"sslmode": "require"})

        return engine

    def get_nonbooked_employees(self):
        engine = self.create_dsql_engine()
        with engine.begin() as conn:
            results = conn.execute(
                text("""SELECT name FROM employees WHERE booked = false""")
            )
            rows = results.fetchall()
            return [row[0] for row in rows]

    def get_booked_employees(self):
        engine = self.create_dsql_engine()
        with engine.begin() as conn:
            results = conn.execute(
                text(
                    """SELECT name, booked, scheduled_time FROM employees WHERE booked = true"""
                )
            )
            rows = results.fetchall()
            return rows

    def update_employee_booking(self, employee_name: str, scheduled_time: str):
        engine = self.create_dsql_engine()
        with engine.begin() as conn:
            results = conn.execute(
                text(
                    """
                    UPDATE employees SET booked = true WHERE name =:user_name;
                    UPDATE employees SET scheduled_time =:scheduled_time WHERE name =:user_name;
                    """
                ),
                {"user_name": employee_name, "scheduled_time": scheduled_time},
            )
            conn.commit()
        return results

    def reset_employees_status(self):
        engine = self.create_dsql_engine()
        with engine.begin() as conn:
            results = conn.execute(
                text(
                    """
                    UPDATE employees SET booked = false;
                    UPDATE employees SET scheduled_time = null;
                    """
                )
            )
        return results
