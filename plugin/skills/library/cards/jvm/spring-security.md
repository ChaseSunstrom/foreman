---
name: spring-security
title: Spring Security
area: jvm
tags: [java, spring, security, auth, oauth2, jwt]
detect: [dep:spring-boot-starter-security, dep:spring-security-core, dep:spring-security-web, dep:spring-boot-starter-oauth2-resource-server]
related: [spring-boot, junit5, mockito, jackson]
---
Spring Security 6 configuration: SecurityFilterChain beans, method security, password encoding, OAuth2 resource server.

## Verify
- `./mvnw -q test` (or `./gradlew test`): security tests with `spring-security-test` pass.
- `curl -si localhost:8080/api/private`: an anonymous call returns 401, not 200 or a login page redirect for an API.
- `curl -si -X POST localhost:8080/api/items`: a state-changing call without a token or CSRF token is refused.
- `./mvnw -q dependency:tree | grep -i security`: one consistent Spring Security version.

## Test first
Use `@WebMvcTest` with `spring-security-test` helpers. Tests sit beside controller tests.
```java
@WebMvcTest(AdminController.class)
@Import(SecurityConfig.class)
class AdminControllerTest {
  @Autowired MockMvc mvc;

  @Test void anonymousIsUnauthorized() throws Exception {
    mvc.perform(get("/admin/users")).andExpect(status().isUnauthorized());
  }
  @Test @WithMockUser(roles = "USER") void userIsForbidden() throws Exception {
    mvc.perform(get("/admin/users")).andExpect(status().isForbidden());
  }
}
```

## Do
- Declare a `SecurityFilterChain` bean with `http.authorizeHttpRequests(a -> a.requestMatchers(...).permitAll().anyRequest().authenticated())`.
- End the matcher list with `anyRequest().authenticated()` (deny by default).
- Hash passwords with `PasswordEncoder` (`BCryptPasswordEncoder` or `Argon2PasswordEncoder`, or `DelegatingPasswordEncoder` via `PasswordEncoderFactories`).
- Use `@EnableMethodSecurity` with `@PreAuthorize` for object-level rules.
- For JWT APIs use `oauth2ResourceServer(o -> o.jwt(Customizer.withDefaults()))` and set `issuer-uri`.
- Keep CSRF on for cookie-session apps; disable it only for stateless token APIs with `SessionCreationPolicy.STATELESS`.
- Configure CORS through `CorsConfigurationSource`, with explicit origins.

## Avoid
- Extending `WebSecurityConfigurerAdapter` or calling `.and()` chains: removed or deprecated; use lambda DSL beans.
- `antMatchers` and `authorizeRequests()`: gone in 6; use `requestMatchers` and `authorizeHttpRequests`.
- `NoOpPasswordEncoder` or plain-text passwords: use a real encoder.
- `csrf().disable()` as a reflex for a browser session app: CSRF returns. Disable only when stateless.
- `permitAll()` on `/**` plus checks in controllers: forgotten routes stay open.
- Trusting role names from the client: `hasRole("ADMIN")` expects the `ROLE_` prefix in authorities; map JWT claims via a `JwtAuthenticationConverter`.
- Hand-rolled JWT parsing with no signature, issuer or audience check.

## Review
- [ ] Default is deny; every public route is listed on purpose.
- [ ] Tests cover anonymous (401), wrong role (403) and allowed paths.
- [ ] No secrets, signing keys or passwords in source.
- [ ] CORS origins and CSRF policy match the client type.
- [ ] Actuator and error endpoints are not accidentally public.
