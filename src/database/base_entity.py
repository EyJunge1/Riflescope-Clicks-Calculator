import sqlite3
from abc import ABC, abstractmethod
from typing import Optional, List, Tuple, Any, Dict
from ..core import db_entities_logger

class DatabaseError(Exception):
    """Custom database exception"""
    pass

class BaseEntity(ABC):
    """Enhanced base class for all database entities"""
    
    def __init__(self, db_cursor):
        if db_cursor is None:
            raise ValueError("Datenbankcursor darf nicht None sein")
        self.db_cursor = db_cursor
        self.table_name = self.get_table_name()
        db_entities_logger.debug(f"Entity initialisiert: {self.__class__.__name__}")
    
    @abstractmethod
    def get_table_name(self) -> str:
        """Return the table name for this entity"""
        pass
    
    @abstractmethod
    def get_insert_fields(self) -> List[str]:
        """Return the fields used for insert operations"""
        pass
    
    def execute_query(self, query: str, params: Tuple = ()) -> List[Tuple]:
        """Execute a query with error handling"""
        try:
            db_entities_logger.debug(f"Executing query: {query} with params: {params}")
            self.db_cursor.execute(query, params)
            return self.db_cursor.fetchall()
        except sqlite3.Error as e:
            db_entities_logger.error(f"Database error in {self.__class__.__name__}: {e}")
            raise DatabaseError(f"Database operation failed: {e}") from e
    
    def execute_single(self, query: str, params: Tuple = ()) -> Optional[Tuple]:
        """Execute a query that returns a single result"""
        try:
            db_entities_logger.debug(f"Executing single query: {query} with params: {params}")
            self.db_cursor.execute(query, params)
            return self.db_cursor.fetchone()
        except sqlite3.Error as e:
            db_entities_logger.error(f"Database error in {self.__class__.__name__}: {e}")
            raise DatabaseError(f"Database operation failed: {e}") from e
    
    def get_by_id(self, entity_id: int) -> Optional[Tuple]:
        """Generic get by ID method"""
        query = f"SELECT * FROM {self.table_name} WHERE id = ?"
        return self.execute_single(query, (entity_id,))
    
    def exists(self, **kwargs) -> bool:
        """Check if entity exists with given criteria"""
        conditions = " AND ".join([f"{key} = ?" for key in kwargs.keys()])
        query = f"SELECT 1 FROM {self.table_name} WHERE {conditions} LIMIT 1"
        result = self.execute_single(query, tuple(kwargs.values()))
        return result is not None
    
    @abstractmethod
    def insert(self, *args, **kwargs):
        """Abstract method for inserting records"""
        pass
    
    @abstractmethod
    def remove(self, *args, **kwargs):
        """Abstract method for removing records"""
        pass
    
    @abstractmethod
    def get_all(self, *args, **kwargs):
        """Abstract method for getting all records"""
        pass
