// a v3 config: literal colours under theme.extend.colors become --color-* tokens
module.exports = {
  content: ["./src/**/*.{html,js}"],
  theme: {
    extend: {
      colors: {
        brand: { DEFAULT: "#3366cc", 500: "#3366cc", "ink-strong": 'rgb(20 30 40)' },
        // muted: '#999999',
        paper: "#f3ece0",
      },
      spacing: { gutter: "24px" },
    },
  },
};
