module.exports = {
	env: {
		browser: true,
		es2021: true,
	},
	extends: 'airbnb-base',
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
	},
	plugins: [
		'html',
	],
}
