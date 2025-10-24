# 🧠 Prolog Parser (Built with Lark)

A syntactic parser for **Prolog** programs built in Python using the [Lark](https://github.com/lark-parser/lark) parsing library.  
This project was originally developed as part of a university coursework and later refined for clarity, usability, and error reporting.

---

## ⚙️ Overview

The parser checks whether a given Prolog program is **syntactically correct** based on a custom-defined grammar implemented in Lark.  
It also provides **meaningful error messages** for common syntax issues, such as:
- Missing opening or closing parentheses
- Unknown or invalid characters
- Unexpected tokens

It can parse multiple `.txt` files (e.g., `1.txt`, `2.txt`, …) in sequence and writes the results to an `output.txt` file.

---

## 🧩 Features

✅ Custom grammar definition for core Prolog constructs  
✅ Detects syntax errors with detailed messages  
✅ Automatically processes multiple input files  
✅ Handles unknown characters and missing parentheses  
✅ Uses [Lark](https://github.com/lark-parser/lark) for grammar-based parsing  
✅ Lightweight and easy to extend  

---

## 🧱 Grammar Structure

The parser defines rules for:
- **Clauses** (`predicate :- predicate_list.`)
- **Queries** (`?- predicate_list.`)
- **Atoms**, **Variables**, **Structures**, and **Numerals**
- **Character classes** (uppercase, lowercase, digits, and special symbols)

Example of grammar definition:
```python
program: [clause (clause)*] query
clause: predicate [":-" predicatelst] "."
query: "?""-" predicatelst "."
...

## 🚀 How to Run
### 1️⃣ Install dependencies
```
pip install lark regex
```
### 2️⃣ Add your Prolog programs
Place your Prolog programs in files named:
``` 1.txt, 2.txt, 3.txt, ... ```
Each should contain a valid (or invalid) Prolog program.
### 3️⃣ Run the parser
```
python prolog.py
```
### 4️⃣ View the output
Check the generated `output.txt` file to see whether each file was syntactically correct or what errors were found.
