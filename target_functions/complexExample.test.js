const { Calculator, sumArray } = require('./complexExample');

describe('Calculator', () => {
  test('constructor initializes memory to zero', () => {
    const calc = new Calculator();
    expect(calc.memory).toBe(0);
  });

  test('add returns sum of two numbers and updates memory', () => {
    const calc = new Calculator();
    const result = calc.add(2, 3);
    expect(result).toBe(5);
    expect(calc.memory).toBe(5);
  });

  test('add throws TypeError for non-number arguments', () => {
    const calc = new Calculator();
    expect(() => calc.add('2', 3)).toThrow(TypeError);
    expect(() => calc.add(2, null)).toThrow('숫자만 허용');
  });

  test('multiplyAsync resolves with multiplication result for numbers', async () => {
    const calc = new Calculator();
    await expect(calc.multiplyAsync(4, 5)).resolves.toBe(20);
  });

  test('multiplyAsync rejects for non-number arguments', async () => {
    const calc = new Calculator();
    await expect(calc.multiplyAsync(4, 'b')).rejects.toBe('숫자만 허용');
  });

  test('divide returns result via callback for valid numbers', (done) => {
    const calc = new Calculator();
    calc.divide(10, 2, (err, result) => {
      expect(err).toBeNull();
      expect(result).toBe(5);
      done();
    });
  });

  test('divide returns error via callback when dividing by zero', (done) => {
    const calc = new Calculator();
    calc.divide(10, 0, (err, result) => {
      expect(err).toBeInstanceOf(Error);
      expect(err.message).toBe('0으로 나눌 수 없음');
      expect(result).toBeUndefined();
      done();
    });
  });

  test('PI returns Math.PI as static method', () => {
    expect(Calculator.PI()).toBe(Math.PI);
  });
});

describe('sumArray', () => {
  test('sums a list of numbers', () => {
    expect(sumArray([1, 2, 3, 4])).toBe(10);
  });
  test('returns 0 for empty array', () => {
    expect(sumArray([])).toBe(0);
  });
  test('throws TypeError for non-array argument', () => {
    expect(() => sumArray(123)).toThrow(TypeError);
    expect(() => sumArray('not array')).toThrow('배열만 허용');
  });
  test('handles arrays with negative numbers and zero', () => {
    expect(sumArray([0, -1, -2, 3])).toBe(0);
  });
});
