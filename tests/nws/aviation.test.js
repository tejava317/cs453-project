const fetch = require('node-fetch');

describe('NWS Aviation API', () => {
  const stationId = 'KJFK'; // JFK 공항
  const tafUrl = `https://api.weather.gov/stations/${stationId}/tafs`;

  test('should return valid TAF data for a known station', async () => {
    const response = await fetch(tafUrl, {
      headers: {
        'User-Agent': 'cs453-project (your@email.com)'
      }
    });
    expect(response.status).toBe(200);

    const data = await response.json();
    expect(data).toHaveProperty('features');
    expect(Array.isArray(data.features)).toBe(true);

    // 최소한 하나 이상의 TAF 데이터가 있어야 함
    expect(data.features.length).toBeGreaterThan(0);

    // 각 feature는 TAF 정보와 geometry를 포함해야 함
    const taf = data.features[0];
    expect(taf).toHaveProperty('properties');
    expect(taf.properties).toHaveProperty('station');
    expect(taf.properties.station).toBe(stationId);
    expect(taf.properties).toHaveProperty('rawText');
    expect(typeof taf.properties.rawText).toBe('string');
  });

  test('should return 404 for an invalid station', async () => {
    const invalidUrl = `https://api.weather.gov/stations/INVALID/tafs`;
    const response = await fetch(invalidUrl, {
      headers: {
        'User-Agent': 'cs453-project (your@email.com)'
      }
    });
    expect(response.status).toBe(404);
  });
});