Distances between terminals are stored in an Excel file which its sheet's name is Distances
it looks like a matrix which first row is destinations and first column is origins and other cells 
are amounts of distances.

Excel files after reading will convert to this data structure in Python:
    { origin_city: ( terminal_delay, { destination_city: travel_time })}
notice: cities that have no way to gether set to a negative amount for example in my samples, i set them as -1

Also terminals delay are stored in that Excel file which its sheet's name is Delays the first row
is cities names and second row is their delay time in minuets 

this program draws the map graph and best ways if the drawan graph looks bad and chaotic you can press regenerate
button on the top side of window to draw it again with new positions

warning1: Sheets name must be: Distances and Delays.

warning2: Distances sheet is necessary but Delays sheet is optional.

warning3: If can't import a terminal delay its value will set to 0.

warning4: Any invalid data(for example a string instead of number in Distance) or any name changes in sheets
or additional empty cell in Excel file is prone to program error. 

warning5: I create 2 Excel data in current folder as examples their names are: map1, map2
