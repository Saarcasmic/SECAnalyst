/** @type {import('tailwindcss').Config} */
export default {
    content: [
        "./index.html",
        "./src/**/*.{js,ts,jsx,tsx}",
    ],
    theme: {
        extend: {
            fontFamily: {
                sovereign: ['"Bodoni Moda"', 'serif'],
                sans: ['"Montserrat"', 'sans-serif'],
                display: ['"Clash Display"', 'sans-serif'],
            },
            colors: {
                obsidian: '#050505',
                gold: '#D4AF37',
                midnight: '#0B0C15',
                glass: 'rgba(255, 255, 255, 0.05)',
            },
            animation: {
                'fade-in': 'fadeIn 0.8s cubic-bezier(0.2, 0.8, 0.2, 1) forwards',
            },
            keyframes: {
                fadeIn: {
                    '0%': { opacity: '0', transform: 'translateY(10px)' },
                    '100%': { opacity: '1', transform: 'translateY(0)' },
                },
            },
        },
    },
    plugins: [
        require('@tailwindcss/typography'),
    ],
}
