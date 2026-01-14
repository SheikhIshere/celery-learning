import React from 'react';
import { MessageSquare, Plus, Menu, X } from 'lucide-react';
import { Session } from '../types';

interface SidebarProps {
  sessions: Session[];
  currentSessionId: number | null;
  onSelectSession: (id: number) => void;
  onNewSession: () => void;
  isOpen: boolean;
  onCloseMobile: () => void;
}

export const Sidebar: React.FC<SidebarProps> = ({ 
  sessions, 
  currentSessionId, 
  onSelectSession, 
  onNewSession,
  isOpen,
  onCloseMobile
}) => {
  return (
    <>
      {/* Mobile Overlay */}
      {isOpen && (
        <div 
          className="fixed inset-0 bg-black/50 z-20 md:hidden"
          onClick={onCloseMobile}
        />
      )}

      {/* Sidebar Content */}
      <aside className={`
        fixed inset-y-0 left-0 z-30 w-64 bg-gray-900 text-gray-100 transform transition-transform duration-300 ease-in-out md:relative md:translate-x-0
        ${isOpen ? 'translate-x-0' : '-translate-x-full'}
      `}>
        <div className="flex flex-col h-full">
          <div className="p-4">
            <button 
              onClick={() => {
                onNewSession();
                onCloseMobile();
              }}
              className="w-full flex items-center gap-2 px-4 py-3 bg-white/10 hover:bg-white/20 border border-white/10 rounded-lg transition-colors text-sm font-medium"
            >
              <Plus size={18} />
              New chat
            </button>
          </div>

          <div className="flex-1 overflow-y-auto px-2 pb-4">
            <div className="text-xs font-semibold text-gray-500 px-3 mb-2 uppercase tracking-wider">
              Recent
            </div>
            {sessions.map((session) => (
              <button
                key={session.id}
                onClick={() => {
                  onSelectSession(session.id);
                  onCloseMobile();
                }}
                className={`w-full text-left px-3 py-3 rounded-lg text-sm mb-1 flex items-center gap-3 transition-colors truncate
                  ${currentSessionId === session.id 
                    ? 'bg-gray-800 text-white' 
                    : 'text-gray-400 hover:bg-gray-800 hover:text-gray-200'
                  }`}
              >
                <MessageSquare size={16} className="shrink-0" />
                <span className="truncate block flex-1">
                  {session.title || `Chat ${session.id}`}
                </span>
              </button>
            ))}
            
            {sessions.length === 0 && (
              <div className="px-3 py-4 text-sm text-gray-500 text-center italic">
                No history yet.
              </div>
            )}
          </div>

          <div className="p-4 border-t border-gray-800">
             <div className="text-xs text-gray-500">
               Django Gemini Chat v1.0
             </div>
          </div>
        </div>
      </aside>
    </>
  );
};