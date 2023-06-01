/** @type {import('next').NextConfig} */
const nextConfig = {
  output: 'export',
  publicRuntimeConfig: {
    baseApiUrl: "http://localhost:8000",
  },
};

module.exports = nextConfig;
