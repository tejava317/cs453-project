import esprima

js_code = '''
function sum(a, b) {
  return a + b;
}
'''
tok = esprima.tokenize(js_code)
print(tok)
ast = esprima.parseScript(js_code)
print(type(ast))
# print(ast)