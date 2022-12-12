from datetime import datetime, timedelta
import bookstore
import sqlite3
import os
import sys


def test_borrow_book():
    con = sqlite3.connect(os.path.join(sys.path[0], 'bookstore.db'))
    cur = con.cursor()
    cur.execute(
        '''CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            isbn TEXT NOT NULL,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            pages INTEGER NOT NULL,
            year TEXT NOT NULL,
            status TEXT DEFAULT "AVAILABLE",
            return_date DATE DEFAULT NULL
        );'''
    )

    bookstore.update_table(cur, bookstore.json_to_list("books.json"))

    return_date_test = datetime.strftime(datetime.now() + timedelta(days=14), "%d-%m-%Y")

    return_date = bookstore.borrow_book(cur, "1", "14")
    assert return_date == return_date_test


def test_return_book():
    con = sqlite3.connect(os.path.join(sys.path[0], 'bookstore.db'))
    cur = con.cursor()
    cur.execute(
        '''CREATE TABLE IF NOT EXISTS books (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            isbn TEXT NOT NULL,
            title TEXT NOT NULL,
            author TEXT NOT NULL,
            pages INTEGER NOT NULL,
            year TEXT NOT NULL,
            status TEXT DEFAULT "AVAILABLE",
            return_date DATE DEFAULT NULL
        );'''
    )

    bookstore.update_table(cur, bookstore.json_to_list("books.json"))

    bookstore.borrow_book(cur, "1", "14")

    fine = bookstore.return_book(cur, "1")

    assert fine is None, f"{fine} doesn't equal None"
