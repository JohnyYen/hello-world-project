# Page snapshot

```yaml
- generic [active] [ref=e1]:
  - button "Open Next.js Dev Tools" [ref=e7] [cursor=pointer]:
    - img [ref=e8]
  - alert [ref=e11]
  - generic [ref=e13]:
    - link "Plataforma Educativa" [ref=e14] [cursor=pointer]:
      - /url: /
      - img [ref=e16]
      - text: Plataforma Educativa
    - generic [ref=e19]:
      - generic [ref=e20]:
        - generic [ref=e21]: Bienvenido de vuelta
        - generic [ref=e22]: Inicia sesión con tus credenciales
      - generic [ref=e25]:
        - group [ref=e26]:
          - generic [ref=e27]: Email
          - textbox "Email" [ref=e28]:
            - /placeholder: m@example.com
        - group [ref=e29]:
          - generic [ref=e30]:
            - generic [ref=e31]: Password
            - link "Forgot your password?" [ref=e32] [cursor=pointer]:
              - /url: "#"
          - textbox "Password" [ref=e33]
        - group [ref=e34]:
          - button "Iniciar Sesión" [ref=e35]
          - paragraph [ref=e36]:
            - text: Don't have an account?
            - link "Sign up" [ref=e37] [cursor=pointer]:
              - /url: /signup
```