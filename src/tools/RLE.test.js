import { Compress, Decompress } from './RLE.js';

describe('RLE Compression', () => {
  test('기본 압축 동작', () => {
    expect(Compress('AAAABBBCCDAA')).toBe('4A3B2C1D2A');
    expect(Compress('AABBCC')).toBe('2A2B2C');
    expect(Compress('ABCD')).toBe('1A1B1C1D');
  });

  test('빈 문자열', () => {
    expect(Compress('')).toBe('');
    expect(Decompress('')).toBe('');
  });

  test('압축 후 복원', () => {
    const original = 'AAABCCDDDD';
    const compressed = Compress(original);
    expect(Decompress(compressed)).toBe(original);
  });

  test('숫자와 문자가 섞인 경우', () => {
    expect(Compress('111222333')).toBe('311322333');
    expect(Decompress('311322333')).toBe('111222333');
  });

  test('특수문자 포함', () => {
    expect(Compress('!!!@@@###')).toBe('3!3@3#');
    expect(Decompress('3!3@3#')).toBe('!!!@@@###');
  });

  test('한 글자만 반복', () => {
    expect(Compress('AAAAA')).toBe('5A');
    expect(Decompress('5A')).toBe('AAAAA');
  });

  test('Decompress가 잘못된 입력을 받을 때', () => {
    expect(Decompress('1A2B')).toBe('ABB');
    expect(Decompress('2A1B3C')).toBe('AABCCC');
  });
});
