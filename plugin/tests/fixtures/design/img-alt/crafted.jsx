export function Avatar({ url, name, big, ...props }) {
  const a = <img src={url} onLoad={() => big > 2} alt={name} />;
  const b = <img {...props} />;
  return <>{a}{b}</>;
}
