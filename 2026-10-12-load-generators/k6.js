// Open loop: k6 starts 400 iterations per second regardless of whether the
// previous ones have finished, which is what constant-arrival-rate means.
import http from 'k6/http';
export const options = {
  scenarios: {
    fixed_rate: {
      executor: 'constant-arrival-rate',
      rate: 400, timeUnit: '1s', duration: '30s',
      preAllocatedVUs: 100, maxVUs: 2000,
    },
  },
};
export default function () { http.get('http://127.0.0.1:8111/'); }
