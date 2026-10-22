export function Avatar({ url, big }) {
  return <img src={url} onLoad={() => big > 2} className="avatar" />; // expect
}
