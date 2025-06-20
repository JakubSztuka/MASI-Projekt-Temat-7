# -*- coding: utf-8 -*-
"""
Created on Tue Jun 17 11:36:56 2025

@author: Jakub
"""

import mysql.connector
from mysql.connector import Error
import json

class DatabaseManager:
    def __init__(self, host, user, password, database):
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None
        self.connect()

    def connect(self):
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            if self.connection.is_connected():
                return True
        except Error as e:
            self.connection = None
        return False

    def close(self):
        if self.connection and self.connection.is_connected():
            self.connection.close()
            self.connection = None

    def _ensure_connection(self):
        if self.connection is None or not self.connection.is_connected():
            if self.connection:
                self.close()
            return self.connect()
        return True

    def insert_operation(self, op_type, param1, param2, converted_structure=None):
        if not self._ensure_connection():
            return False
        try:
            cursor = self.connection.cursor()
            
            if converted_structure:
                json_data = json.dumps(converted_structure)
                query = "INSERT INTO operations (type, param1, param2, converted_structure) VALUES (%s, %s, %s, %s)"
                cursor.execute(query, (op_type, param1, param2, json_data))
            else:
                query = "INSERT INTO operations (type, param1, param2) VALUES (%s, %s, %s)"
                cursor.execute(query, (op_type, param1, param2))
            
            self.connection.commit()
            return True
        except Error as e:
            self.close()
            return False

    def get_all_operations(self):
        if not self._ensure_connection():
            return []
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = "SELECT id, type, param1, param2, converted_structure FROM operations"
            cursor.execute(query)
            operations = cursor.fetchall()
            
            for op in operations:
                if op['converted_structure']:
                    op['converted_structure'] = json.loads(op['converted_structure'])
            return operations
        except Error as e:
            self.close()
            return []

    def get_operation_by_id(self, op_id):
        if not self._ensure_connection():
            return None
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = "SELECT id, type, param1, param2, converted_structure FROM operations WHERE id = %s"
            cursor.execute(query, (op_id,))
            operation = cursor.fetchone()
            
            if operation and operation['converted_structure']:
                operation['converted_structure'] = json.loads(operation['converted_structure'])
            return operation
        except Error as e:
            self.close()
            return None

    def get_converted_operations(self):
        if not self._ensure_connection():
            return []
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = "SELECT id, type, param1, param2, converted_structure FROM operations WHERE converted_structure IS NOT NULL"
            cursor.execute(query)
            operations = cursor.fetchall()
            
            for op in operations:
                if op['converted_structure']:
                    op['converted_structure'] = json.loads(op['converted_structure'])
            return operations
        except Error as e:
            self.close()
            return []

    def get_operations_by_type(self, op_type):
        if not self._ensure_connection():
            return []
        try:
            cursor = self.connection.cursor(dictionary=True)
            query = "SELECT id, type, param1, param2, converted_structure FROM operations WHERE type = %s AND converted_structure IS NULL"
            cursor.execute(query, (op_type,))
            operations = cursor.fetchall()
            return operations
        except Error as e:
            self.close()
            return []

    def delete_operation(self, op_id):
        if not self._ensure_connection():
            return False
        try:
            cursor = self.connection.cursor()
            query = "DELETE FROM operations WHERE id = %s"
            cursor.execute(query, (op_id,))
            self.connection.commit()
            if cursor.rowcount > 0:
                return True
            else:
                return False
        except Error as e:
            self.close()
            return False