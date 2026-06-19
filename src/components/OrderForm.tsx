import { useState, useRef } from "react";
import Icon from "@/components/ui/icon";

const BACKEND_URL = "https://functions.poehali.dev/f1734664-2817-4ae0-b55d-063881924103";

const SERVICE_OPTIONS = [
  "Нейро-фотосессия",
  "Телеграм-стикеры",
  "Фотосессия + стикеры",
];

export default function OrderForm() {
  const [name, setName] = useState("");
  const [contact, setContact] = useState("");
  const [service, setService] = useState(SERVICE_OPTIONS[0]);
  const [wish, setWish] = useState("");
  const [photo, setPhoto] = useState<File | null>(null);
  const [status, setStatus] = useState<"idle" | "loading" | "success" | "error">("idle");
  const fileRef = useRef<HTMLInputElement>(null);

  const handlePhoto = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files?.[0]) setPhoto(e.target.files[0]);
  };

  const toBase64 = (file: File): Promise<string> =>
    new Promise((resolve, reject) => {
      const reader = new FileReader();
      reader.onload = () => resolve((reader.result as string).split(",")[1]);
      reader.onerror = reject;
      reader.readAsDataURL(file);
    });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setStatus("loading");

    let photoBase64: string | null = null;
    let photoName: string | undefined;
    if (photo) {
      photoBase64 = await toBase64(photo);
      photoName = photo.name;
    }

    try {
      const res = await fetch(BACKEND_URL, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, contact, service, wish, photo: photoBase64, photo_name: photoName }),
      });
      if (res.ok) {
        setStatus("success");
        setName(""); setContact(""); setWish(""); setPhoto(null);
        if (fileRef.current) fileRef.current.value = "";
      } else {
        setStatus("error");
      }
    } catch {
      setStatus("error");
    }
  };

  return (
    <section id="order" className="bg-white px-6 py-20">
      <div className="max-w-xl mx-auto">
        <h3 className="uppercase text-sm tracking-wide text-neutral-500 mb-3">Оставить заявку</h3>
        <h2 className="text-3xl md:text-4xl font-bold text-neutral-900 mb-10 leading-tight">
          Расскажите о себе — <br />мы сделаем всё остальное
        </h2>

        {status === "success" ? (
          <div className="flex flex-col items-center gap-4 py-16 text-center">
            <Icon name="CheckCircle" size={48} className="text-green-500" />
            <p className="text-xl font-semibold text-neutral-900">Заявка отправлена!</p>
            <p className="text-neutral-500">Мы свяжемся с вами в ближайшее время.</p>
            <button
              onClick={() => setStatus("idle")}
              className="mt-4 uppercase text-sm tracking-wide underline text-neutral-500 hover:text-neutral-900 transition-colors"
            >
              Отправить ещё
            </button>
          </div>
        ) : (
          <form onSubmit={handleSubmit} className="flex flex-col gap-5">
            <div className="flex flex-col gap-1">
              <label className="text-xs uppercase tracking-wide text-neutral-500">Имя *</label>
              <input
                required
                value={name}
                onChange={e => setName(e.target.value)}
                placeholder="Как вас зовут?"
                className="border border-neutral-200 px-4 py-3 text-sm outline-none focus:border-neutral-900 transition-colors bg-neutral-50"
              />
            </div>

            <div className="flex flex-col gap-1">
              <label className="text-xs uppercase tracking-wide text-neutral-500">Телефон или Telegram *</label>
              <input
                required
                value={contact}
                onChange={e => setContact(e.target.value)}
                placeholder="+7 900 000 00 00 или @username"
                className="border border-neutral-200 px-4 py-3 text-sm outline-none focus:border-neutral-900 transition-colors bg-neutral-50"
              />
            </div>

            <div className="flex flex-col gap-1">
              <label className="text-xs uppercase tracking-wide text-neutral-500">Тип услуги</label>
              <select
                value={service}
                onChange={e => setService(e.target.value)}
                className="border border-neutral-200 px-4 py-3 text-sm outline-none focus:border-neutral-900 transition-colors bg-neutral-50 cursor-pointer"
              >
                {SERVICE_OPTIONS.map(o => (
                  <option key={o} value={o}>{o}</option>
                ))}
              </select>
            </div>

            <div className="flex flex-col gap-1">
              <label className="text-xs uppercase tracking-wide text-neutral-500">Пожелание</label>
              <textarea
                value={wish}
                onChange={e => setWish(e.target.value)}
                placeholder="Стиль, настроение, детали..."
                rows={3}
                className="border border-neutral-200 px-4 py-3 text-sm outline-none focus:border-neutral-900 transition-colors bg-neutral-50 resize-none"
              />
            </div>

            <div className="flex flex-col gap-1">
              <label className="text-xs uppercase tracking-wide text-neutral-500">Фото (необязательно)</label>
              <div
                onClick={() => fileRef.current?.click()}
                className="border border-dashed border-neutral-300 px-4 py-6 flex flex-col items-center gap-2 cursor-pointer hover:border-neutral-900 transition-colors bg-neutral-50"
              >
                <Icon name="Upload" size={24} className="text-neutral-400" />
                <p className="text-sm text-neutral-500">
                  {photo ? photo.name : "Нажмите, чтобы загрузить фото"}
                </p>
              </div>
              <input
                ref={fileRef}
                type="file"
                accept="image/*"
                onChange={handlePhoto}
                className="hidden"
              />
            </div>

            {status === "error" && (
              <p className="text-red-500 text-sm">Что-то пошло не так. Попробуйте ещё раз.</p>
            )}

            <button
              type="submit"
              disabled={status === "loading"}
              className="bg-black text-white px-6 py-4 text-sm uppercase tracking-wide transition-all duration-300 hover:bg-neutral-800 disabled:opacity-50 flex items-center justify-center gap-2"
            >
              {status === "loading" ? (
                <>
                  <Icon name="Loader2" size={16} className="animate-spin" />
                  Отправляем...
                </>
              ) : (
                "Отправить заявку"
              )}
            </button>
          </form>
        )}
      </div>
    </section>
  );
}
