const gulp = require('gulp');
const postcss = require('gulp-postcss');
const tailwindcss = require('tailwindcss');
const autoprefixer = require('autoprefixer');
const cleanCSS = require('gulp-clean-css');
const uglify = require('gulp-uglify');

// Paths to your CSS, JavaScript, and HTML files
const paths = {
    styles: {
        src: 'static/src/main.css',
        dest: 'static/dist/css/'
    },
    scripts: {
        src: 'node_modules/flowbite/dist/flowbite.js',
        dest: 'static/dist/js/'
    },
    html: {
        src: 'static/*.html' // Update the path to your HTML files
    }
};

// Task to process and minify CSS with Tailwind CSS and Autoprefixer
function styles() {
    return gulp.src(paths.styles.src)
        .pipe(postcss([
            tailwindcss,
            autoprefixer
        ]))
        .pipe(cleanCSS())
        .pipe(gulp.dest(paths.styles.dest));
}

// Task to copy and minify Flowbite JavaScript
function scripts() {
    return gulp.src(paths.scripts.src)
        .pipe(uglify())
        .pipe(gulp.dest(paths.scripts.dest));
}

// Task to watch HTML files for changes
function html() {
    return gulp.src(paths.html.src)
        .pipe(postcss([
            tailwindcss,
            autoprefixer
        ]))
        .pipe(cleanCSS())
        .pipe(gulp.dest('static/dist/')); // Update the destination folder for HTML files
}

// Watch files for changes
function watchFiles() {
    gulp.watch(paths.styles.src, styles);
    gulp.watch(paths.scripts.src, scripts);
    gulp.watch(paths.html.src, html); // Add watch for HTML files
}

// Define complex tasks
const build = gulp.series(gulp.parallel(styles, scripts, html)); // Add html task to build task
const watch = gulp.series(build, watchFiles);

// Export tasks
exports.styles = styles;
exports.scripts = scripts;
exports.html = html; // Export html task
exports.watch = watch;
exports.build = build;
exports.default = build;