import React from "react";

type IconProps = React.SVGProps<SVGSVGElement> & { size?: number; strokeWidth?: number };

const paths: Record<string, React.ReactNode> = {
  Home: <><path d="M3 10.5 12 3l9 7.5"/><path d="M5 9.5V21h14V9.5M9 21v-7h6v7"/></>,
  Users: <><circle cx="9" cy="8" r="3"/><path d="M3.5 20c.5-4 2.3-6 5.5-6s5 2 5.5 6M16 5.5a3 3 0 0 1 0 5.9M16 14c2.7.4 4.2 2.2 4.5 6"/></>,
  ClipboardList: <><rect x="5" y="4" width="14" height="17" rx="2"/><path d="M9 4V2h6v2M9 10h6M9 14h6M9 18h4"/></>,
  BookOpen: <><path d="M3 5.5A3.5 3.5 0 0 1 6.5 2H11v18H6.5A3.5 3.5 0 0 0 3 23.5Z"/><path d="M21 5.5A3.5 3.5 0 0 0 17.5 2H13v18h4.5a3.5 3.5 0 0 1 3.5 3.5Z"/></>,
  Settings: <><circle cx="12" cy="12" r="3"/><path d="M19.4 15a1.7 1.7 0 0 0 .3 1.9l.1.1-2.8 2.8-.1-.1a1.7 1.7 0 0 0-1.9-.3 1.7 1.7 0 0 0-1 1.6v.2h-4V21a1.7 1.7 0 0 0-1-1.6 1.7 1.7 0 0 0-1.9.3l-.1.1L4.2 17l.1-.1a1.7 1.7 0 0 0 .3-1.9A1.7 1.7 0 0 0 3 14H2.8v-4H3a1.7 1.7 0 0 0 1.6-1 1.7 1.7 0 0 0-.3-1.9L4.2 7 7 4.2l.1.1A1.7 1.7 0 0 0 9 4.6a1.7 1.7 0 0 0 1-1.6v-.2h4V3a1.7 1.7 0 0 0 1 1.6 1.7 1.7 0 0 0 1.9-.3l.1-.1L19.8 7l-.1.1a1.7 1.7 0 0 0-.3 1.9 1.7 1.7 0 0 0 1.6 1h.2v4H21a1.7 1.7 0 0 0-1.6 1Z"/></>,
  Plus: <path d="M12 5v14M5 12h14"/>,
  ChevronRight: <path d="m9 18 6-6-6-6"/>,
  ArrowLeft: <path d="m12 19-7-7 7-7M5 12h14"/>,
  Check: <path d="m5 12 4 4L19 6"/>,
  X: <path d="M6 6l12 12M18 6 6 18"/>,
  Mic: <><rect x="9" y="3" width="6" height="12" rx="3"/><path d="M5 11a7 7 0 0 0 14 0M12 18v3M9 21h6"/></>,
  Square: <rect x="6" y="6" width="12" height="12" rx="1"/>,
  Play: <path d="m8 5 11 7-11 7Z"/>,
  Pause: <><path d="M9 5v14M15 5v14"/></>,
  Calendar: <><rect x="3" y="5" width="18" height="16" rx="2"/><path d="M7 3v4M17 3v4M3 10h18"/></>,
  Send: <><path d="m22 2-7 20-4-9-9-4Z"/><path d="M22 2 11 13"/></>,
  Trash2: <><path d="M4 7h16M9 7V4h6v3M7 7l1 14h8l1-14M10 11v6M14 11v6"/></>,
  ArrowUp: <path d="m6 11 6-6 6 6M12 5v14"/>,
  ArrowDown: <path d="m6 13 6 6 6-6M12 19V5"/>,
  RotateCcw: <><path d="M3 12a9 9 0 1 0 3-6.7L3 8"/><path d="M3 3v5h5"/></>,
  MessageSquare: <path d="M21 15a4 4 0 0 1-4 4H8l-5 3V7a4 4 0 0 1 4-4h10a4 4 0 0 1 4 4Z"/>,
  TrendingUp: <><path d="m3 17 6-6 4 4 8-9"/><path d="M15 6h6v6"/></>,
  PenLine: <><path d="m4 20 4.5-1 10-10-3.5-3.5-10 10Z"/><path d="M13.5 7 17 10.5M4 22h16"/></>,
  Languages: <><path d="M4 5h7M7.5 3v2M5 9c2.5 3 5 4.5 8 5M11 5c-1 4-3.5 7-7 9"/><path d="m14 21 4-10 4 10M15.5 17h5"/></>,
  Target: <><circle cx="12" cy="12" r="9"/><circle cx="12" cy="12" r="5"/><circle cx="12" cy="12" r="1"/></>,
  CheckCircle2: <><circle cx="12" cy="12" r="9"/><path d="m8 12 3 3 6-7"/></>,
  Circle: <circle cx="12" cy="12" r="9"/>,
  Pencil: <><path d="m4 20 4.5-1 10-10-3.5-3.5-10 10Z"/><path d="M13.5 7 17 10.5"/></>,
  Volume2: <><path d="M5 10H2v4h3l4 4V6Z"/><path d="M13 9a4 4 0 0 1 0 6M16 6a8 8 0 0 1 0 12"/></>,
  Sparkles: <><path d="m12 3 1.2 3.8L17 8l-3.8 1.2L12 13l-1.2-3.8L7 8l3.8-1.2ZM5 15l.8 2.2L8 18l-2.2.8L5 21l-.8-2.2L2 18l2.2-.8ZM19 14l.7 1.8 1.8.7-1.8.7L19 19l-.7-1.8-1.8-.7 1.8-.7Z"/></>,
};

function makeIcon(name: string) {
  return function Icon({ size = 24, strokeWidth = 2, color, ...props }: IconProps) {
    return (
      <svg width={size} height={size} viewBox="0 0 24 24" fill="none" stroke={color || "currentColor"}
        strokeWidth={strokeWidth} strokeLinecap="round" strokeLinejoin="round" aria-hidden="true" {...props}>
        {paths[name]}
      </svg>
    );
  };
}

export const Home = makeIcon("Home");
export const Users = makeIcon("Users");
export const ClipboardList = makeIcon("ClipboardList");
export const BookOpen = makeIcon("BookOpen");
export const Settings = makeIcon("Settings");
export const Plus = makeIcon("Plus");
export const ChevronRight = makeIcon("ChevronRight");
export const ArrowLeft = makeIcon("ArrowLeft");
export const Check = makeIcon("Check");
export const X = makeIcon("X");
export const Mic = makeIcon("Mic");
export const Square = makeIcon("Square");
export const Play = makeIcon("Play");
export const Pause = makeIcon("Pause");
export const Calendar = makeIcon("Calendar");
export const Send = makeIcon("Send");
export const Trash2 = makeIcon("Trash2");
export const ArrowUp = makeIcon("ArrowUp");
export const ArrowDown = makeIcon("ArrowDown");
export const RotateCcw = makeIcon("RotateCcw");
export const MessageSquare = makeIcon("MessageSquare");
export const TrendingUp = makeIcon("TrendingUp");
export const PenLine = makeIcon("PenLine");
export const Languages = makeIcon("Languages");
export const Target = makeIcon("Target");
export const CheckCircle2 = makeIcon("CheckCircle2");
export const Circle = makeIcon("Circle");
export const Pencil = makeIcon("Pencil");
export const Volume2 = makeIcon("Volume2");
export const Sparkles = makeIcon("Sparkles");
