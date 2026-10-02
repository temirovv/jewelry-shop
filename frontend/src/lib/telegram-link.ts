// Brauzerdan kirganlarni Telegram Mini App'ga yo'naltirish uchun havolalar.
// Bot'da "Main Mini App" sozlangan, shuning uchun t.me/<bot>?startapp=<param>
// do'konni darhol ochadi va <param> WebApp ichida start_param bo'lib keladi.

// Env'dan olinmaydi: VITE_BOT_USERNAME .env fayllarda placeholder
// ("your_bot_username") bo'lib qolgan va tekshirilmagan — ochiq ma'lumot,
// qat'iy yozish xavfsizroq
export const BOT_USERNAME = "Ziyorauz_bot";

// Telegram cheklovi: startapp faqat [A-Za-z0-9_-], ko'pi bilan 512 belgi
const START_PARAM_RE = /^[A-Za-z0-9_-]{1,512}$/;

function toBase64Url(text: string): string {
  const bytes = new TextEncoder().encode(text);
  let binary = "";
  bytes.forEach((b) => (binary += String.fromCharCode(b)));
  return btoa(binary).replace(/\+/g, "-").replace(/\//g, "_").replace(/=+$/, "");
}

function fromBase64Url(param: string): string {
  const base64 = param.replace(/-/g, "+").replace(/_/g, "/");
  const binary = atob(base64.padEnd(Math.ceil(base64.length / 4) * 4, "="));
  const bytes = Uint8Array.from(binary, (ch) => ch.charCodeAt(0));
  return new TextDecoder().decode(bytes);
}

// Sahifa yo'li (masalan /product/krem) slug'da kirill harflari bo'lishi
// mumkinligi sababli base64url ko'rinishida uzatiladi
export function buildStartParam(path: string): string | null {
  if (!path || path === "/") return null;
  const param = toBase64Url(path);
  return START_PARAM_RE.test(param) ? param : null;
}

// Faqat ilova ichidagi yo'l qabul qilinadi ("//evil.com" kabi qiymatlar emas)
export function parseStartParam(param: string | undefined): string | null {
  if (!param || !START_PARAM_RE.test(param)) return null;
  try {
    const path = fromBase64Url(param);
    if (!path.startsWith("/") || path.startsWith("//")) return null;
    return path;
  } catch {
    return null;
  }
}

// Telegram'ning "kimga yuborish" oynasi (chat tanlash) uchun havola
export function telegramShareUrl(link: string, text: string): string {
  return `https://t.me/share/url?url=${encodeURIComponent(link)}&text=${encodeURIComponent(text)}`;
}

export function telegramAppLink(path = "/"): string {
  const param = buildStartParam(path);
  const base = `https://t.me/${BOT_USERNAME}?startapp`;
  return param ? `${base}=${param}` : base;
}
