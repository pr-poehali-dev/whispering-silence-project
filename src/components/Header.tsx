interface HeaderProps {
  className?: string;
}

export default function Header({ className }: HeaderProps) {
  return (
    <header className={`absolute top-0 left-0 right-0 z-10 p-6 ${className ?? ""}`}>
      <div className="flex justify-between items-center">
        <div className="text-[#1A9494] text-sm uppercase tracking-wide">bediff</div>
        <nav className="flex gap-8">
          <a
            href="#about"
            className="text-[#1A9494] hover:text-[#2ABFBF] transition-colors duration-300 uppercase text-sm"
          >
            Как это работает
          </a>
          <a
            href="#contact"
            className="text-[#1A9494] hover:text-[#2ABFBF] transition-colors duration-300 uppercase text-sm"
          >
            Заказать
          </a>
        </nav>
      </div>
    </header>
  );
}