# ThalapathyVJ Programming Language
![image](https://github.com/user-attachments/assets/a2e1a8d0-d6e9-44d9-9776-8a7a3f841ced)

## Introduction
ThalapathyVJ is a fan-made programming language inspired by the dialogues, songs, and titles from Actor Vijay's films. This language serves as a creative tribute to the actor and includes a variety of features such as mathematical operations, string manipulation, data types, logical operators, and more.

## Who is Vijay?

Vijay, is an Indian actor and playback singer who works in Tamil cinema. In a career spanning over three decades, Vijay has acted in 68 films. He has been referred to as "Thalapathy". 

For more details, click on it -> [Vijay (actor) on Wikipedia](https://en.wikipedia.org/wiki/Vijay_(actor))

---

## Origin of Idea

I got this idea from two languages: **Bhai language** and **Rajini++**. I got inspired from them and made this language.


## Syntax Reference Table

### String Manipulation Functions

| Function                     | Reference                          | Purpose                        |
|------------------------------|------------------------------------|--------------------------------|
| `en_nenjil_kudi_irukkum`      | Iconic dialogue from *Thalapathy Vijay* | Prints a statement.            |
| `yeru_yeru_muneru`            | Song reference from *Sachin*        | Converts a string to uppercase. |
| `life_is_very_short_nanba`    | Song reference from *Master*        | Converts a string to lowercase. |
| `nee_poo_nee_vaa`             | Comedy dialogue from *Madurey*      | Replaces a substring in a string. |
| `meenuku_kaal_irukka_illaya` | Comedy dialogue from *Madurey*      | Checks if a string is alphanumeric. |
| `meenuku_kaal_irukka`         | Comedy dialogue from *Madurey*      | Checks if a string is alphabetic. |
| `ips_vijaykumar`              | Dialogue reference from *Theri*     | Capitalizes a string.          |
| `thamizhan`                   | Movie title from *Thamizhan*        | Joins strings.                 |
| `unma_kadhal_naa_sollu`       | Dialogue reference from *Shahjahan* | Finds the index of a word in a string. |
| `kaakhi`                      | Comedy dialogue from *Jilla*        | Splits text into parts.        |

### Data Types Functions

| Function                     | Reference                          | Purpose                        |
|------------------------------|------------------------------------|--------------------------------|
| `naa_guru_than_pesuren`       | Dialogue reference from *Azhagiya Thamizh Magan* | Represents a string data type. |
| `coca_cola`                   | Song reference from *Bhagavathi*    | Represents a double data type. |
| `nei_eduthutu_vaa`            | Comedy dialogue from *Gilli*       | Represents an integer data type. |
| `nei_nei_eduthutu_vaa`        | Comedy dialogue from *Gilli*       | Represents a float data type.  |
| `naa_thanda_leo`              | Dialogue reference from *Leo*      | Boolean data type for True.   |
| `naa_avan_illa`              | Dialogue reference from *Leo*      | Boolean data type for False.  |

### Arithmetic Operators

| Operator/Function | Reference | Purpose                           |
|-------------------|-----------|-----------------------------------|
| `+=`, `-=`, `*=`, `/=` | None      | Arithmetic assignment operators.  |
| `+`, `-`, `*`, `/` | None      | Basic arithmetic operators.       |
| `%=`               | None      | Modulus assignment operator.      |
| `**`               | None      | Exponentiation operator.          |
| `**=`              | None      | Exponentiation assignment operator.|

### Comparison and Logical Operators

| Operator/Function | Reference | Purpose                             |
|-------------------|-----------|-------------------------------------|
| `==`              | None      | Equality comparison operator.       |
| `!=`              | None      | Inequality comparison operator.     |
| `>`               | None      | Greater than operator.              |
| `<`               | None      | Less than operator.                 |
| `>=`              | None      | Greater than or equal comparison.   |
| `<=`              | None      | Less than or equal comparison.      |
| `sura`            | Movie title from *Sura* | Logical AND operator.              |
| `kuruvi`          | Movie title from *Kuruvi* | Logical OR operator.               |
| `villu`           | Movie title from *Villu* | Logical NOT operator.              |

### Bitwise Operators

| Operator   | Reference | Purpose                           |
|------------|-----------|-----------------------------------|
| `&`        | None      | Bitwise AND operator.             |
| `\|`        | None      | Bitwise OR operator.              |
| `~`        | None      | Bitwise NOT operator.             |
| `>>`       | None      | Right shift operator.             |
| `<<`       | None      | Left shift operator.              |

### Miscellaneous

| Function/Operator | Reference | Purpose                           |
|-------------------|-----------|-----------------------------------|
| `++`              | None      | Increment operator.               |
| `--`              | None      | Decrement operator.               |
| `=`               | None      | Assignment operator.              |
| `%`               | None      | Modulus operator.                 |

## Example Programs

### Print Statement

#### Code
![image](https://github.com/user-attachments/assets/2bcd1943-ecc7-44ac-b9fb-9ec237298758)

#### Output
![image](https://github.com/user-attachments/assets/251ab43e-317b-4228-85c6-d1c827e0e3ec)


### Calculator

#### Code
![image](https://github.com/user-attachments/assets/d014c1e0-512e-4e08-a781-21b1daff60a8)

#### Output
![image](https://github.com/user-attachments/assets/c7e21eb9-8a67-4cf3-8951-bccbcdb6856e)


### String Manipulation

#### Code
![image](https://github.com/user-attachments/assets/866e4f93-3251-4edc-b1a5-0e2f3aebca5a)

#### Output
![image](https://github.com/user-attachments/assets/023c4c01-5b5a-44bc-ac47-72ff4599fe66)

## Implementation and Execution

1. **Clone the Git Repository:**
https://github.com/Ajay7616/ThalapathyVJ_Programming_Language.git


2. **Write your code** in any text editor and save the file with the `.tvj` extension.

3. **Execute the code**:
Open the terminal and run the following command:
python interpreter.py filename.tvj


## How It Works

- **Lexer.py**: Tokenizes the code (e.g., `int`, `float`, `string`) based on the custom keywords and syntax of ThalapathyVJ.
- **Parser.py**: Handles the logical processing and evaluation of the tokens according to the programming language's rules.
- **Interpreter.py**: Uses both the lexer and parser to process the code and produce the output.
- **test.tvj**: Sample file for testing the code written in ThalapathyVJ language.

### Added Advantage

By changing the tokenizing words in the lexer and adjusting the extension in the interpreter file, you can create your own programming language.
