const assert = require('assert');
const sum = require('../../funtion.js');

// Core tests
assert.strictEqual(sum(2, 3), 5);
assert.strictEqual(sum(-2, -3), -5);
assert.strictEqual(sum(0, 3), 3);
assert.strictEqual(sum(2, 0), 2);
assert.strictEqual(sum(0, 0), 0);
assert.strictEqual(sum(1.5, 2.5), 4.0);

// Missing arguments
assert.ok(Number.isNaN(sum(2)));
assert.ok(Number.isNaN(sum()));

// String arguments
assert.strictEqual(sum('2', '3'), '23');
assert.strictEqual(sum(2, '3'), '23');
assert.strictEqual(sum('2', 3), '23');

// Null arguments
assert.strictEqual(sum(null, 3), 3);
assert.strictEqual(sum(2, null), 2);
assert.strictEqual(sum(null, null), 0);

// Undefined arguments
assert.ok(Number.isNaN(sum(undefined, 3)));
assert.ok(Number.isNaN(sum(2, undefined)));
assert.ok(Number.isNaN(sum(undefined, undefined)));

// Extra arguments
assert.strictEqual(sum(1, 2, 3, 4), 3);

// New test cases (additional coverage)
assert.ok(Number.isNaN(sum({}, 3)));
assert.strictEqual(sum([], 3), '3');
assert.strictEqual(sum(true, 2), 3);
assert.strictEqual(sum(false, 2), 2);
assert.strictEqual(sum(Number.MAX_SAFE_INTEGER, 1), Number.MAX_SAFE_INTEGER + 1);
assert.ok(Number.isNaN(sum(NaN, 2)));
assert.ok(Number.isNaN(sum(2, NaN)));

// Edge: Boolean + String
assert.strictEqual(sum(true, '3'), '13');
assert.strictEqual(sum('3', false), '30');

console.log('All sum() tests passed!');
