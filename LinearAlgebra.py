import copy

class Matrix:
    def __init__(self, *args, fill=0, identity=None, _random=None):
        arg1 = args[0]
        if isinstance(arg1,int):
            self._matrix = [[fill for num in range(arg1)] for row in range(arg1)]
        elif isinstance(arg1, tuple):
            self._matrix = [[fill for num in range(arg1[1])] for row in range(arg1[0])]
        elif isinstance(arg1, list) or isinstance(arg1, set):
            if isinstance(arg1[0], list) or isinstance(arg1[0], set):
                self._matrix = arg1
            else:
                raise TypeError('Each row of Matrix needs to be in separate nested list')
        else:
            raise TypeError('Can only create a Matrix from ints, tuples, and lists')

        self.size = self.get_size()
        if len(self._matrix) != self.size[0]:
            raise Exception('Matrix must be rectangular')
        else:
            for row in self._matrix:
                if len(row) != self.size[1]:
                    raise Exception('Matrix must be rectangular')

        if identity:
            self.set_identity()

    def __str__(self):
        string = ''
        for row in self._matrix:
            string += '|'
            for num in row:
                string += f' {num} '
            string += '|\n'
        return string

    def __iter__(self):
        for row in self._matrix:
            yield row

    def __getitem__(self, key):
        if isinstance(key, tuple):
            matrix_slice = self._matrix[key[0]][key[1]]
            if isinstance(key[0], int) and isinstance(key[1], int):
                return matrix_slice
            elif isinstance(key[1], int):
                return Matrix(matrix_slice)
            elif isinstance(key[1], slice):
                rows = self._matrix[key[0]]
                matrix_slice = [row[key[1]] for row in rows]
                return Matrix(matrix_slice)

    def __setitem__(self, key, value):
        if isinstance(key, tuple):
            if isinstance(value, int) or isinstance(value, float):
                if isinstance(key[0], int) and isinstance(key[1], int):
                    self._matrix[key[0]][key[1]] = value
                elif isinstance(key[0], slice) or isinstance(key[1], slice):
                    key = [slice(key[index],key[index]+1) if isinstance(key[index], int) else key[index] for index in range(0,2)]
                    start0, stop0, step0 = key[0].indices(self.size[0])
                    start1, stop1, step1 = key[1].indices(self.size[1])
                    self._matrix = [[value if index >= start1 and index < stop1 and index % step1 == 0 else self._matrix[row][index] for index in range(0, self.size[1])] if row >= start0 and row < stop0 and row % step0 == 0 else self._matrix[row] for row in range(0, self.size[0])]
            if isinstance(value, Matrix):
                key = [slice(key[index],key[index]+1) if isinstance(key[index], int) else key[index] for index in range(0,2)]
                start0, stop0, step0 = key[0].indices(self.size[0])
                start1, stop1, step1 = key[1].indices(self.size[1])
                self._matrix = [[value._matrix[row-start0][index-start1] if index >= start1 and index < stop1 and index % step1 == 0 else self._matrix[row][index] for index in range(0, self.size[1])] if row >= start0 and row < stop0 and row % step0 == 0 else self._matrix[row] for row in range(0, self.size[0])]

    def __deepcopy__(self, memodict={}):
        return Matrix([[value for value in row] for row in self.__iter__()])

    def __add__(self, other):
        temp = copy.deepcopy(self)
        if isinstance(other, int) or isinstance(other, float):
            temp = Matrix([[num+other for num in row] for row in temp])
            return temp
        elif isinstance(other, Matrix):
            row, column = 0, 0
            try:
                for row in range(self.size[0]):
                    for column in range(self.size[1]):
                        temp.__setitem__((row, column), self.__getitem__((row, column)) + other.__getitem__((row, column)))
                return temp
            except:
                raise ValueError('Matrices must be same size')
        else:
            raise TypeError('Only int, float, and Matrix can be added from Matrix')

    def __sub__(self, other):
        temp = copy.deepcopy(self)
        if isinstance(other, int) or isinstance(other, float):
            temp = Matrix([[num-other for num in row] for row in temp])
            return temp
        elif isinstance(other, Matrix):
            try:
                for row in range(self.size[0]):
                    for column in range(self.size[1]):
                        temp.__setitem__((row, column), self.__getitem__((row, column)) - other.__getitem__((row, column)))
                return temp
            except:
                raise ValueError('Matrices must be same size')
        else:
            raise TypeError('Only int, float, and Matrix can be subtracted from Matrix')

    def __mul__(self, other):
        temp = copy.deepcopy(self)
        if isinstance(other, int) or isinstance(other, float):
            temp = Matrix([[num*other for num in row] for row in temp])
            return temp
        elif isinstance(other, Matrix):
            if self.size[1] == other.size[0]:
                temp = Matrix((other.size[1], self.size[0]))
                for row in range(self.size[0]):
                    for column in range(other.size[1]):
                        temp.__setitem__((row, column), sum([self.__getitem__((row, index)) * other.__getitem__((index, column)) for index in range(self.size[1])]))
                return temp
            else:
                raise Exception('Matrices are not right sizes to be multiplied')
        else:
            raise TypeError('Only int, float, and Matrix can be multiplied with Matrix')

    def get_size(self):
        return (len(self._matrix), len(self._matrix[0]))

    def set_size(self, size, fill=0):
        if size[0] > self.size[0]:
            new_row = [fill for value in range(self.size[1])]
            for _ in range(size[0] - self.size[0]):
                self._matrix.append(new_row)
        elif size[0] < self.size[0]:
            self._matrix = self._matrix[:size[0]-self.size[0]]
        if size[1] > self.size[1]:
            for row in self._matrix:
                for _ in range(size[1]-self.size[1]):
                    row.append(fill)
        elif size[1] < self.size[1]:
            self._matrix = [row[:size[1]-self.size[1]] for row in self._matrix]
        self.size = self.get_size

    def set_identity(self):
        self._matrix = [[1 if column == row else 0 for column in range(self.size[1])] for row in range(self.size[0])]

    def delete(self, row=None, column=None, _return=None):
        if row or row == 0:
            self._matrix.pop(row)
        elif column or column == 0:
            for row in self._matrix:
                row.pop(column)
        if _return:
            return self
        self.size = self.get_size

    def transpose(self):
        self._matrix = [[self._matrix[row][column] for row in range(self.size[0])] for column in range(self.size[1])]

    def det(self):
        return det(self)

class Vector(Matrix):
    def __init__(self, *args):
        if isinstance(args[0], int):
            matrix_arg = (1, args[0])
        elif isinstance(args[0], list):
            matrix_arg = [args[0]]
        else:
            raise Exception('Can only create a Vector from int or list')

        super().__init__(matrix_arg)

    def __iter__(self):
        for value in self._matrix[0]:
            yield value

    def __getitem__(self, key):
        return super().__getitem__((1, key))

    def magnitude(self):
        return sum([value**2 for value in self._matrix[0]])**.5

def det(matrix):
    matrix.size = matrix.get_size()
    if matrix.size == (2,2):
        return matrix[0,0]*matrix[1,1] - matrix[0,1]*matrix[1,0]
    else:
        return sum([matrix[0, column]*det(matrix[1:,:].delete(column=column, _return=True))*(-1)**column for column in range(matrix.size[1])])

def solve(matrix, vector):
    if vector.size[0] == 1:
        vector.transpose()
    temp = [copy.deepcopy(matrix) for _ in range(matrix.size[1])]
    solutions = [None for key in range(matrix.size[1])]
    detA = det(matrix)
    for column in range(3):
        temp[column][:,column] = vector
        solutions[column] = det(temp[column])/detA
    return solutions
