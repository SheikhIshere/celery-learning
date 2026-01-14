import React from 'react';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';

interface MessageProps {
  text: string;
}

const Message: React.FC<MessageProps> = ({ text }) => {
  return (
    <div className="message p-2 border-b">
      <ReactMarkdown remarkPlugins={[remarkGfm]}>
        {text}
      </ReactMarkdown>
    </div>
  );
};

export default Message;
