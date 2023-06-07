module.exports = {
	env: {
		browser: true,
		es2021: true,
	},
	extends: ['airbnb-base'],
	overrides: [
	],
	parserOptions: {
		ecmaVersion: 'latest',
		sourceType: 'module',
	},
	rules: {
		'no-restricted-syntax': 'off',
		semi: ['error', 'never'],
		'no-tabs': 'off',
		indent: ['error', 'tab'],
		'no-param-reassign': 0,
		'no-unused-vars': 0,
		'arrow-parens': ['error', 'as-needed', { requireForBlockBody: true }],
	},
	plugins: [
		'html',
		'eslint-plugin-engagement-platform-webapp/preprocessors.js',
	],

}
