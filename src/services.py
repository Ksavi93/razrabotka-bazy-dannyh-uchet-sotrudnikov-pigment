from db import get_connection


def fetch_employees():
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("""
            SELECT id, Name, Surname, ThirdName, Age, Sex, DateAdm,
                   Position, Department, PhoneNumber, EMail, Head, Photo
            FROM EMPLOYEE
            ORDER BY id DESC
        """)
        return cursor.fetchall()


def add_employee(data):
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("""
            INSERT INTO EMPLOYEE
            (Name, Surname, ThirdName, Age, Sex, DateAdm, Position, Department,
             PhoneNumber, EMail, Head, Photo)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, data)
        connection.commit()


def update_employee(emp_id, data):
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("""
            UPDATE EMPLOYEE
            SET Name=?, Surname=?, ThirdName=?, Age=?, Sex=?, DateAdm=?,
                Position=?, Department=?, PhoneNumber=?, EMail=?, Head=?, Photo=?
            WHERE id=?
        """, (*data, emp_id))
        connection.commit()


def delete_employee(emp_id, reason, date_value):
    with get_connection() as connection:
        cursor = connection.cursor()
        cursor.execute("DELETE FROM EMPLOYEE WHERE id=?", (emp_id,))
        cursor.execute(
            "INSERT INTO ARCHIVE (id, prichina, date) VALUES (?, ?, ?)",
            (emp_id, reason, date_value)
        )
        connection.commit()
