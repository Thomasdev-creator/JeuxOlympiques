/**
 * This is a minimal config.
 *
 * If you need the full config, get it from here:
 * https://unpkg.com/browse/tailwindcss@latest/stubs/defaultConfig.stub.js
 */

module.exports = {
    content: [
        /**
         * HTML. Paths to Django template files that will contain Tailwind CSS classes.
         */

        /*  Templates within theme app (<tailwind_app_name>/templates), e.g. base.html. */
        '../templates/**/*.html',

        /*
         * Main templates directory of the project (BASE_DIR/templates).
         * Adjust the following line to match your project structure.
         */
        '../../templates/**/*.html',

        /*
         * Templates in other django apps (BASE_DIR/<any_app_name>/templates).
         * Adjust the following line to match your project structure.
         */
        '../../**/templates/**/*.html',

        /**
         * JS: If you use Tailwind CSS in JavaScript, uncomment the following lines and make sure
         * patterns match your project structure.
         */
        /* JS 1: Ignore any JavaScript in node_modules folder. */
        // '!../../**/node_modules',
        /* JS 2: Process all JavaScript files in the project. */
        // '../../**/*.js',

        /**
         * Python: If you use Tailwind CSS classes in Python, uncomment the following line
         * and make sure the pattern below matches your project structure.
         */
        // '../../**/*.py'
    ],
    /*
1. Arrière-plan de l'application
2. Arrière-plan subtil
3. Arrière-plan de l'élément d'interface utilisateur
4. Arrière-plan de l'élément d'interface utilisateur survolé
5. Arrière-plan de l'élément d'interface utilisateur actif/sélectionné
6. Bordures et séparateurs subtils
7. Bordure d'élément d'interface utilisateur et anneaux de focus
8. Bordure d'élément d'interface utilisateur survolé
9. Arrière-plans solides
10. Arrière-plans solides survolés
11. Texte à faible contraste
12. Texte à fort contraste
     */
    theme: {
        extend: {
            colors: {
                AppBackground: '#fdfdfe',
                SubtleBackground: '#f7f9ff',
                UIElementBackground: '#edf2fe',
                HoveredUIElementBackground: '#e1e9ff',
                ActiveSelectedUIElementBackground: '#d2deff',
                SubtleBordersandSeparators: '#c1d0ff',
                UIElementBorderAndFocusRings: '#abbdf9',
                HoveredUIElementBorder: '#8da4ef',
                SolidBackgrounds: '#3e63dd',
                HoveredSolidBackgrounds: '#3358d4',
                LowContrastText: '#3a5bc7',
                HighContrastText: '#1f2d5c',

                DarkAppBackground: '#11131f',
                DarkSubtleBackground: '#141726',
                DarkUIElementBackground: '#182449',
                DarkHoveredUIElementBackground: '#1d2e62',
                DarkActiveSelectedUIElementBackground: '#253974',
                DarkSubtleBordersandSeparators: '#304384',
                DarkUIElementBorderAndFocusRings: '#3a4f97',
                DarkHoveredUIElementBorder: '#435db1',
                DarkSolidBackgrounds: '#3e63dd',
                DarkHoveredSolidBackgrounds: '#5472e4',
                DarkLowContrastText: '#9eb1ff',
                DarkHighContrastText: '#d6e1ff',
            },
            fontSize: {
                custom: '66px',
                clampUsm: 'clamp(5, 2, 10)',
                clampSm: 'clamp(20px, 3vw, 50px)',
                clampMd: 'clamp(30px, 4vw, 60px)',
                clampLg: 'clamp(40px, 5vw, 70px)',
            },
            gridTemplateColumns: {
                menu: '100px 1fr 100px'
            },
        },
    },
    plugins: [
        /**
         * '@tailwindcss/forms' is the forms plugin that provides a minimal styling
         * for forms. If you don't like it or have own styling for forms,
         * comment the line below to disable '@tailwindcss/forms'.
         */
        require('@tailwindcss/forms'),
        require('@tailwindcss/typography'),
        require('@tailwindcss/aspect-ratio'),
    ],
}
