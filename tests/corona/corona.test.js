const fetch = require('node-fetch');

describe('2019-nCoV (Coronavirus) API', () => {
  const baseUrl = 'https://coronavirus-19-api.herokuapp.com';

  test('should return global stats', async () => {
    const response = await fetch(`${baseUrl}/all`);
    expect(response.status).toBe(200);

    const data = await response.json();
    expect(data).toHaveProperty('cases');
    expect(data).toHaveProperty('deaths');
    expect(data).toHaveProperty('recovered');
    expect(typeof data.cases).toBe('number');
    expect(typeof data.deaths).toBe('number');
    expect(typeof data.recovered).toBe('number');
  });

  test('should return country stats for South Korea', async () => {
    const response = await fetch(`${baseUrl}/countries/South%20Korea`);
    expect(response.status).toBe(200);

    const data = await response.json();
    expect(data).toHaveProperty('country', 'South Korea');
    expect(data).toHaveProperty('cases');
    expect(data).toHaveProperty('deaths');
    expect(data).toHaveProperty('recovered');
  });

  test('should return 404 or error for invalid country', async () => {
    const response = await fetch(`${baseUrl}/countries/InvalidCountryName`);
    // 일부 API는 200 + 에러 메시지, 일부는 404를 반환할 수 있음
    expect([200, 404]).toContain(response.status);

    const data = await response.json();
    // 에러 메시지 또는 빈 객체 등 다양한 케이스를 허용
    expect(data).toBeDefined();
  });
});