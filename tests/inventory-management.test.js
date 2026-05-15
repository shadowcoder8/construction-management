const test = require('node:test');
const assert = require('node:assert');
const fs = require('node:fs');
const vm = require('node:vm');

test('addMaterial displays alert on non-ok response', async () => {
    const code = fs.readFileSync('frontend/inventory-management.js', 'utf8');

    let alertCalledWith = null;
    let consoleErrorCalled = false;

    const sandbox = {
        document: {
            getElementById: () => ({ addEventListener: () => {}, value: '' }),
            querySelector: () => ({ innerHTML: '', appendChild: () => {}, getElementsByTagName: () => [] }),
        },
        fetch: async (url, options) => {
            return {
                ok: false,
                status: 500
            };
        },
        alert: (msg) => {
            alertCalledWith = msg;
        },
        console: {
            error: (msg, err) => {
                consoleErrorCalled = true;
            },
            log: () => {}
        },
        setTimeout: setTimeout,
        clearTimeout: clearTimeout,
        confirm: () => true,
        window: { location: { href: '' } },
        JSON: JSON
    };

    vm.createContext(sandbox);
    vm.runInContext(code, sandbox);

    await sandbox.addMaterial({ name: 'Test' });

    assert.strictEqual(alertCalledWith, 'Failed to add material.');
    assert.strictEqual(consoleErrorCalled, true);
});
