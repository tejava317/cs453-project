const exportedFunction = require('./myFunction');

describe('f', () => {
  test('exports a function named f', () => {
    expect(typeof exportedFunction).toBe('function');
    expect(exportedFunction.name).toBe('f');
  });

  test('기본 동작: true 반환', () => {
    expect(exportedFunction()).toBe(true);
  });

  test('f ignores extra arguments and still returns true', () => {
    expect(exportedFunction(1, 2, 3)).toBe(true);
  });

  test('f has no parameters', () => {
    expect(exportedFunction.length).toBe(0);
  });

  test('f strictly returns boolean true', () => {
    expect(exportedFunction()).toBe(true);
    expect(exportedFunction()).not.toBe(false);
    expect(typeof exportedFunction()).toBe('boolean');
  });
});
