const sum = require('./myFunction');

describe('sum function unit tests', () => {
  test('adds two positive numbers', () => {
    expect(sum(2, 3)).toBe(5);
  });

  test('adds zero and a number', () => {
    expect(sum(0, 5)).toBe(5);
    expect(sum(7, 0)).toBe(7);
  });

  test('adds negative and positive number', () => {
    expect(sum(-4, 10)).toBe(6);
    expect(sum(9, -3)).toBe(6);
  });

  test('adds two negative numbers', () => {
    expect(sum(-5, -8)).toBe(-13);
  });

  test('adds decimal numbers', () => {
    expect(sum(2.5, 3.1)).toBeCloseTo(5.6);
  });

  test('adds large numbers', () => {
    expect(sum(1_000_000, 2_000_000)).toBe(3_000_000);
  });

  test('adds string arguments', () => {
    expect(sum('2', '3')).toBe('23');
  });

  test('missing arguments', () => {
    expect(sum(5)).toBeNaN();
    expect(sum()).toBeNaN();
  });
});