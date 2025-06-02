const { Calculator, sumArray } = require('./complexExample');

describe('Calculator', () => {
  test('constructor initializes memory to 0', () => {
    const calc = new Calculator();
    expect(calc.memory).toBe(0);
  });

  test('add method adds two numbers correctly', () => {
    const calc = new Calculator();
    expect(calc.add(5, 3)).toBe(8);
    expect(calc.memory).toBe(8);
  });

  test('add method throws TypeError for non-number inputs', () => {
    const calc = new Calculator();
    expect(() => calc.add('5', 3)).toThrow(TypeError);
    expect(() => calc.add(5, '3')).toThrow(TypeError);
    expect(() => calc.add(null, 3)).toThrow(TypeError);
  });

  test('multiplyAsync returns correct product', async () => {
    const calc = new Calculator();
    const result = await calc.multiplyAsync(4, 5);
    expect(result).toBe(20);
  });

  test('multiplyAsync rejects with non-number inputs', async () => {
    const calc = new Calculator();
    await expect(calc.multiplyAsync('4', 5)).rejects.toBe('숫자만 허용');
    await expect(calc.multiplyAsync(4, '5')).rejects.toBe('숫자만 허용');
  });

  test('divide method divides two numbers correctly', (done) => {
    const calc = new Calculator();
    calc.divide(10, 2, (err, result) => {
      expect(err).toBeNull();
      expect(result).toBe(5);
      done();
    });
  });

  test('divide method handles division by zero', (done) => {
    const calc = new Calculator();
    calc.divide(10, 0, (err, result) => {
      expect(err).toBeInstanceOf(Error);
      expect(err.message).toBe('0으로 나눌 수 없음');
      expect(result).toBeUndefined();
      done();
    });
  });

  test('static PI method returns Math.PI', () => {
    expect(Calculator.PI()).toBe(Math.PI);
  });

  test('Calculator memory updates correctly after operations', () => {
    const calc = new Calculator();
    calc.add(5, 5);
    expect(calc.memory).toBe(10);
    calc.divide(calc.memory, 2, (err, result) => {
      expect(result).toBe(5);
    });
  });

  test('Async operations can be chained', async () => {
    const calc = new Calculator();
    const product = await calc.multiplyAsync(4, 5);
    expect(product).toBe(20);
    const sum = calc.add(product, 10);
    expect(sum).toBe(30);
    expect(calc.memory).toBe(30);
  });

  test('Calculator handles floating point calculations', () => {
    const calc = new Calculator();
    expect(calc.add(0.1, 0.2)).toBeCloseTo(0.3);
  });

  test('Calculator handles large numbers', () => {
    const calc = new Calculator();
    const largeNum = Number.MAX_SAFE_INTEGER;
    expect(calc.add(largeNum, 1)).toBe(largeNum + 1);
  });
});

describe('sumArray', () => {
  test('sumArray correctly sums array elements', () => {
    expect(sumArray([1, 2, 3, 4, 5])).toBe(15);
    expect(sumArray([-1, -2, 3])).toBe(0);
    expect(sumArray([0.1, 0.2, 0.3])).toBeCloseTo(0.6);
    expect(sumArray([])).toBe(0);
  });

  test('sumArray throws TypeError for non-array inputs', () => {
    expect(() => sumArray(123)).toThrow(TypeError);
    expect(() => sumArray('array')).toThrow(TypeError);
    expect(() => sumArray(null)).toThrow(TypeError);
    expect(() => sumArray(undefined)).toThrow(TypeError);
    expect(() => sumArray({})).toThrow(TypeError);
  });

  test('sumArray handles arrays with non-number values', () => {
    expect(() => sumArray([1, '2', 3])).not.toThrow();
  });

  test('sumArray handles negative numbers', () => {
    expect(sumArray([-1, -2, -3])).toBe(-6);
  });

  test('sumArray handles mixed positive and negative', () => {
    expect(sumArray([1, -2, 3, -4])).toBe(-2);
  });

  test('sumArray handles large numbers', () => {
    expect(sumArray([1000000, 2000000, 3000000])).toBe(6000000);
  });

  test('sumArray handles zero as an element', () => {
    expect(sumArray([1, 2, 0, 3])).toBe(6);
  });
});
