### Ferramentas disponíveis ao LLM

#### 1) get_route
**Descrição:** calcula rota indoor determinística.
**Parâmetros:**
```json
{
  "type": "object",
  "properties": {
    "destino": {"type": "string"},
    "acessibilidade": {"type": "boolean", "default": false},
    "origem": {"type": "string"}
  },
  "required": ["destino"]
}
