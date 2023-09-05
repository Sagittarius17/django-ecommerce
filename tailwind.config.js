module.exports = {
    mode: 'jit',
    purge: [
        './**/*.html',
        './**/*.js',
    ],
    theme: {
        extend: {
            // backdropBlur: {
            //     'none': 'blur(0)',
            //     'blur': 'blur(5px)',
            //     'more-blur': 'blur(10px)',
            //     // ... you can add more custom values
            //  }
        },
    },
    variants: {},
    plugins: [],
}
