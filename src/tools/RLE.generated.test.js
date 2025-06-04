const RLE = require('../Compression/RLE');

describe('RLE Basic Functionality', () => {
  test('should encode a simple string correctly', () => {
    expect(RLE('aaa')).toBe('a3');
    expect(RLE('aaabbc')).toBe('a3b2c1');
    expect(RLE('abc')).toBe('a1b1c1');
  });

  test('should handle empty strings', () => {
    expect(RLE('')).toBe('');
  });

  test('should handle single character strings', () => {
    expect(RLE('a')).toBe('a1');
  });

  test('should handle alternating characters', () => {
    expect(RLE('ababab')).toBe('a1b1a1b1a1b1');
  });
});

describe('RLE Edge Cases', () => {
  test('should handle strings with special characters', () => {
    expect(RLE('!!!')).toBe('!3');
    expect(RLE('a!@#')).toBe('a1!1@1#1');
    expect(RLE('   ')).toBe(' 3');
  });

  test('should handle strings with numbers', () => {
    expect(RLE('111222')).toBe('1322');
    expect(RLE('a111b')).toBe('a13b1');
  });

  test('should handle strings with mixed case', () => {
    expect(RLE('AAAaaa')).toBe('A3a3');
    expect(RLE('AaAa')).toBe('A1a1A1a1');
  });

  test('should handle strings with whitespace', () => {
    expect(RLE('a b  c')).toBe('a1 1b1 2c1');
    expect(RLE('\n\n\t')).toBe('\n2\t1');
  });
});

describe('RLE Boundary Conditions', () => {
  test('should handle strings with repeating and non-repeating sections', () => {
    expect(RLE('aaabcdd')).toBe('a3b1c1d2');
    expect(RLE('abcdddeee')).toBe('a1b1c1d3e3');
  });

  test('should handle Unicode characters', () => {
    expect(RLE('😀😀😀')).toBe('😀3');
    expect(RLE('🚀✨🚀✨')).toBe('🚀1✨1🚀1✨1');
  });

  test('should handle very large counts correctly', () => {
    const largeString = 'a'.repeat(1000);
    expect(RLE(largeString)).toBe('a1000');
  });
});

describe('RLE Integration Tests', () => {
  test('should encode real-world data patterns correctly', () => {
    // CSV-like data with repeating fields
    expect(RLE('data,data,data,value,value')).toBe('d1a1t1a1,1d1a1t1a1,1d1a1t1a1,1v1a1l1u1e1,1v1a1l1u1e1');
    // JSON-like pattern
    expect(RLE('{{{{}}}}}')).toBe('{4}4}1');
  });
});
