import test from 'node:test';
import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';

function page() {
  const html = fs.readFileSync(new URL('../index.html', import.meta.url), 'utf8');
  const scripts = [...html.matchAll(/<script(?:\s[^>]*)?>([\s\S]*?)<\/script>/gi)].map(x => x[1]).filter(x => x.trim());
  const elements = new Map();
  function element(id) {
    if (!elements.has(id)) elements.set(id, { value: '5', textContent: '', innerText: '', classList: { add() {}, remove() {} }, width: 256, height: 256, getContext() { return { clearRect() {}, fillRect() {} }; } });
    return elements.get(id);
  }
  const context = vm.createContext({ document: { getElementById: element }, console });
  for (const script of scripts) vm.runInContext(script, context, { timeout: 1000 });
  return { context, element };
}
test('local preview advances the real automaton and reports its scope', () => {
  const p = page(); p.element('actionAmount').value = '500'; p.context.executeAction();
  assert.equal(p.element('cycleCounter').innerText, 'Cycle: 1');
  assert.match(p.element('actionStatus').textContent, /Local demo preview: 500/);
  assert.match(p.element('actionStatus').textContent, /No wallet connection, transaction or invariant verification occurred/);
  assert.doesNotMatch(p.element('actionStatus').textContent, /Tx:|Success!|Invariant Verified/);
});
test('invalid quantities cannot advance the automaton or claim a transaction', () => {
  for (const value of ['', '0', '-1', '1.5', '1000001', 'NaN', '<img src=x onerror=alert(1)>']) {
    const p = page(); p.element('actionAmount').value = value; p.context.executeAction();
    assert.equal(p.element('cycleCounter').innerText, '');
    assert.match(p.element('actionStatus').textContent, /No action was performed/);
  }
});
test('wallet preview never presents a connected address', () => {
  const p = page(); p.context.toggleWallet();
  assert.equal(p.element('walletBtnText').textContent, 'Demo preview active (no wallet)');
  p.context.toggleWallet(); assert.equal(p.element('walletBtnText').textContent, 'Preview wallet UI');
});
