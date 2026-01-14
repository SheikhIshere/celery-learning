import React from 'react';
import { Bot, User } from 'lucide-react';

interface MessageBubbleProps {
  content: string;
  isUser: boolean;
  timestamp?: string;
}

export const MessageBubble: React.FC<MessageBubbleProps> = ({ content, isUser, timestamp }) => {
  return (
    <div className={`flex w-full mb-6 ${isUser ? 'justify-end' : 'justify-start'}`}>
      <div className={`flex max-w-[85%] md:max-w-[70%] ${isUser ? 'flex-row-reverse' : 'flex-row'} items-end gap-2`}>
        
        {/* Avatar */}
        <div className={`w-8 h-8 rounded-full flex items-center justify-center shrink-0 mb-1 
          ${isUser ? 'bg-purple-600 text-white' : 'bg-green-600 text-white'}`}>
          {isUser ? <User size={16} /> : <Bot size={16} />}
        </div>

        {/* Bubble */}
        <div className={`relative px-4 py-3 text-sm md:text-base leading-relaxed shadow-sm
          ${isUser 
            ? 'bg-gradient-to-r from-purple-500 to-pink-500 text-white rounded-2xl rounded-br-sm' 
            : 'bg-white border border-gray-100 text-gray-800 rounded-2xl rounded-bl-sm'
          }`}>
          <div className="whitespace-pre-wrap">{content}</div>
          {timestamp && (
            <div className={`text-[10px] mt-1 opacity-70 ${isUser ? 'text-purple-100' : 'text-gray-400'}`}>
              {new Date(timestamp).toLocaleTimeString([], {hour: '2-digit', minute:'2-digit'})}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};