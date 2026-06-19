export default function Pricing() {
  return (
    <section id="pricing" className="bg-neutral-900 px-6 py-20">
      <div className="max-w-4xl mx-auto">
        <h3 className="uppercase text-sm tracking-wide text-neutral-500 mb-3">Стоимость</h3>
        <h2 className="text-3xl md:text-4xl font-bold text-white mb-12 leading-tight">
          Простые цены — никаких скрытых платежей
        </h2>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
          <div className="border border-neutral-700 p-8 flex flex-col gap-4 hover:border-white transition-colors duration-300">
            <p className="uppercase text-xs tracking-wide text-neutral-500">Услуга</p>
            <h3 className="text-2xl font-bold text-white">Телеграм-стикеры</h3>
            <p className="text-neutral-400 text-sm leading-relaxed flex-1">
              Загрузите своё фото — получите уникальный стикерпак с вашим персонажем и разными эмоциями. Готово к публикации в Telegram.
            </p>
            <div className="border-t border-neutral-700 pt-4 flex items-end gap-2">
              <span className="text-5xl font-bold text-white">150</span>
              <span className="text-neutral-400 mb-2">₽</span>
            </div>
            <a
              href="#order"
              className="bg-white text-black px-6 py-3 text-sm uppercase tracking-wide text-center transition-all duration-300 hover:bg-neutral-200"
            >
              Заказать стикеры
            </a>
          </div>

          <div className="border border-white p-8 flex flex-col gap-4 relative">
            <p className="uppercase text-xs tracking-wide text-neutral-500">Популярное</p>
            <h3 className="text-2xl font-bold text-white">AI Фотосессия</h3>
            <p className="text-neutral-400 text-sm leading-relaxed flex-1">
              Профессиональные портреты в любом стиле — деловые, креативные, атмосферные. Без студии и фотографа, результат за несколько минут.
            </p>
            <div className="border-t border-neutral-700 pt-4 flex items-end gap-2">
              <span className="text-5xl font-bold text-white">250</span>
              <span className="text-neutral-400 mb-2">₽</span>
            </div>
            <a
              href="#order"
              className="bg-white text-black px-6 py-3 text-sm uppercase tracking-wide text-center transition-all duration-300 hover:bg-neutral-200"
            >
              Заказать фотосессию
            </a>
          </div>
        </div>
      </div>
    </section>
  );
}
