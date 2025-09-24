# Graphical Route Optimizer

> Read Excel distance/delay data, build a network graph of terminals, and visualize best routes.

This project reads **Excel files** containing city-to-city distances and optional terminal delays, converts them into a convenient Python data structure, and draws a graph that highlights best paths between terminals.

---

## Table of contents

* [Input data format](#input-data-format)
* [Internal data structure](#internal-data-structure)
* [Features](#features)
* [Warnings & constraints](#warnings--constraints)
* [Installation & dependencies](#installation--dependencies)
* [Usage](#usage)
* [Example](#example)
* [Samples](#samples)
* [Preview](#preview)

---

## Input data format

**Files** must be Excel files (.xlsx or .xls) with the following sheets:

### `Distances` (Required)

* This sheet represents a **matrix** of travel times between terminals.
* The **first row** contains destination city names.
* The **first column** contains origin city names.
* Each other cell contains the travel time between the origin (row) and destination (column).
* If there is **no route** between two terminals, set the value to `-1`.

**Example ****`Distances`**** sheet** (matrix):

|       | CityB | CityC | CityD |
| ----- | ----- | ----- | ----- |
| CityA | 10    | -1    | 25    |
| CityB | 10    | 0     | 15    |
| CityC | -1    | 5     | 20    |

### `Delays` (Optional)

* This sheet stores **terminal delay times (minutes)**.
* The **first row** contains city names.
* The **second row** contains the delay value (in minutes) for each city.

**Example ****`Delays`**** sheet**:

| CityA | CityB | CityC | CityD |
| ----- | ----- | ----- | ----- |
| 5     | 2     | 0     | 7     |

If the `Delays` sheet is missing or a delay value cannot be read for a city, that city's delay defaults to `0`.

---

## Internal data structure

After loading, the Excel data is converted to a Python dictionary with the following shape:

```python
{
    "CityA": (delay_time, {"CityB": travel_time, "CityC": travel_time, ...}),
    "CityB": (delay_time, {"CityA": travel_time, "CityD": travel_time, ...}),
    # ...
}
```

**Example**:

```python
{
    "CityA": (5, {"CityB": 10, "CityC": -1, "CityD": 25}),
    "CityB": (2, {"CityA": 10, "CityC": 0, "CityD": 15}),
}
```

Notes:

* A travel time of `-1` indicates no connection.
* Terminal delays are integers (minutes); missing delays default to `0`.

---

## Features

* Reads `Distances` (required) and `Delays` (optional) from Excel.
* Converts data to a Python-friendly dictionary representation.
* Draws a graph of terminals (nodes) and routes (edges).
* Highlights best routes / shortest paths.
* If the drawn graph appears chaotic, press the **Regenerate** button in the GUI to redraw with a new node layout.

---

## Warnings & constraints

1. **Sheet names are required to be exactly** `Distances` and `Delays`.
2. `Distances` sheet is **mandatory**; `Delays` is optional.
3. If a terminal delay cannot be imported, its value will be set to `0`.
4. **Invalid data** (for example, strings in distance cells or unexpected empty cells) or renaming sheets will likely cause runtime errors.
5. Keep the matrix rectangular and avoid extra empty cells or stray headers—these are common causes of errors.

---

## Installation & dependencies

This project requires Python 3.8+ (recommended). Install the typical dependencies with:

```bash
pip install -r requirements.txt
```


---

## Usage

1. Place your Excel file(s) in the project folder (e.g. `map1.xlsx`, `map2.xlsx`).
2. Run the main script:

```bash
python main.py
```

3. A GUI window will open and show the graph. Use the **Regenerate** button on the top side of the window to draw the graph again with new node positions if the layout looks messy.

---

## Example

Given an Excel file `map1.xlsx` containing a `Distances` sheet and an optional `Delays` sheet, the program will:

1. Parse the `Distances` matrix into the internal dictionary structure.
2. Read delays from `Delays` (if present) and default any missing values to `0`.
3. Build a graph where nodes are cities and edges are travel times.
4. Display the graph and compute/highlight best paths.

---

## Samples

Two example Excel files are included in the repository root for convenience:

* `map1.xlsx`
* `map2.xlsx`

These demonstrate the expected format and can be used to test the program quickly.

---

## Preview

![Demo GIF](asset/preview.gif)
