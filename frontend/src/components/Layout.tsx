import React from 'react';
import { LayoutGrid, ShoppingCart, Package, BarChart3, Settings, LogOut, Bell } from 'lucide-react';

export const Layout: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  return (
    <div className="flex h-screen overflow-hidden">
      {/* Sidebar */}
      <aside className="w-64 glass border-r border-white/10 hidden md:flex flex-col">
        <div className="p-6">
          <h1 className="text-xl font-bold bg-gradient-to-r from-primary to-purple-400 bg-clip-text text-transparent">
            Engine Market
          </h1>
        </div>
        <nav className="flex-1 px-4 space-y-2 mt-4">
          <NavItem icon={LayoutGrid} label="Dashboard" active />
          <NavItem icon={ShoppingCart} label="Sales" />
          <NavItem icon={Package} label="Inventory" />
          <NavItem icon={BarChart3} label="Finance" />
        </nav>
        <div className="p-4 mt-auto border-t border-white/10">
          <NavItem icon={Settings} label="Settings" />
          <NavItem icon={LogOut} label="Logout" className="text-red-400 hover:bg-red-400/10" />
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 overflow-y-auto relative">
        {/* Header */}
        <header className="h-16 glass sticky top-0 z-10 flex items-center justify-between px-8">
          <h2 className="font-semibold text-lg">Market Overview</h2>
          <div className="flex items-center gap-4">
            <button className="p-2 hover:bg-white/5 rounded-full relative">
              <Bell size={20} />
              <span className="absolute top-2 right-2 w-2 h-2 bg-red-500 rounded-full"></span>
            </button>
            <div className="w-8 h-8 rounded-full bg-primary flex items-center justify-center font-bold text-xs">
              AD
            </div>
          </div>
        </header>

        <div className="p-8">
          {children}
        </div>
      </main>
    </div>
  );
};

const NavItem = ({ icon: Icon, label, active, className }: any) => (
  <button className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-all duration-200 ${
    active ? 'bg-primary/20 text-primary border border-primary/20' : 'hover:bg-white/5 text-foreground/70 hover:text-foreground'
  } ${className}`}>
    <Icon size={18} />
    <span className="font-medium">{label}</span>
  </button>
);
