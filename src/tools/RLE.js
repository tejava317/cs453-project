// RLE (Run Length Encoding) compression and decompression
function Compress(str) {
  let compressed = '';
  let count = 1;
  for (let i = 0; i < str.length; i++) {
    if (str[i] !== str[i + 1]) {
      compressed += count + str[i];
      count = 1;
      continue;
    }
    count++;
  }
  return compressed;
}

function Decompress(str) {
  let decompressed = '';
  let match = [...str.matchAll(/(\d+)(\D)/g)];
  match.forEach((item) => {
    let [count, char] = [item[1], item[2]];
    decompressed += char.repeat(count);
  });
  return decompressed;
}

module.exports = { Compress, Decompress };
