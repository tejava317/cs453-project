// 복잡한 예시: 다양한 기능, 예외, 비동기, 콜백, 클래스, 모듈 패턴 등 포함

class Calculator {
  constructor() {
    this.memory = 0;
  }

  add(a, b) {
    if (typeof a !== 'number' || typeof b !== 'number') throw new TypeError('숫자만 허용');
    this.memory = a + b;
    return this.memory;
  }

  async multiplyAsync(a, b) {
    return new Promise((resolve, reject) => {
      setTimeout(() => {
        if (typeof a !== 'number' || typeof b !== 'number') return reject('숫자만 허용');
        resolve(a * b);
      }, 100);
    });
  }

  divide(a, b, cb) {
    if (b === 0) return cb(new Error('0으로 나눌 수 없음'));
    cb(null, a / b);
  }

  static PI() {
    return Math.PI;
  }
}

function sumArray(arr) {
  if (!Array.isArray(arr)) throw new TypeError('배열만 허용');
  return arr.reduce((acc, cur) => acc + cur, 0);
}

module.exports = { Calculator, sumArray };
