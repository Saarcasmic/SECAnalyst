import { useState, useRef, useEffect } from 'react';
import axios from 'axios';
import { Bot, User, ArrowUp, TrendingUp, AlertTriangle, FileText, ChevronDown, ChevronRight, Loader2, Sparkles } from 'lucide-react';
import { motion, AnimatePresence } from 'framer-motion';
import FinancialChart from './FinancialChart';
import { Text } from './components/ui/Text';
import { Button } from './components/ui/Button';
import ReactMarkdown from 'react-markdown';
import remarkGfm from 'remark-gfm';
import BackgroundWave from './components/BackgroundWave';
import ApiKeyModal from './components/ApiKeyModal';

// Thinking Component
const ThinkingDropdown = ({ steps, isOpen, setIsOpen, isDone }) => {
    if (steps.length === 0) return null;

    return (
        <div className="mb-4 w-full max-w-xl">
            <button
                onClick={() => setIsOpen(!isOpen)}
                className="flex items-center gap-2 text-xs uppercase tracking-[0.15em] text-gold/80 hover:text-gold transition-colors w-full text-left"
            >
                {isOpen ? <ChevronDown className="w-4 h-4" /> : <ChevronRight className="w-4 h-4" />}
                <span className="font-medium flex items-center gap-2">
                    {isDone ? "Thought Process" : "Thinking..."}
                    {!isDone && <Sparkles className="w-3 h-3 animate-pulse" />}
                </span>
            </button>

            <AnimatePresence>
                {isOpen && (
                    <motion.div
                        initial={{ height: 0, opacity: 0 }}
                        animate={{ height: "auto", opacity: 1 }}
                        exit={{ height: 0, opacity: 0 }}
                        className="overflow-hidden"
                    >
                        <div className="pl-4 border-l-2 border-gold/20 mt-2 space-y-2 py-1">
                            {steps.map((step, idx) => (
                                <motion.div
                                    key={idx}
                                    initial={{ x: -10, opacity: 0 }}
                                    animate={{ x: 0, opacity: 1 }}
                                    className="text-xs text-gray-400 font-mono"
                                >
                                    {step}
                                </motion.div>
                            ))}
                        </div>
                    </motion.div>
                )}
            </AnimatePresence>
        </div>
    );
};

// Holographic Card Component
const HolographicCard = ({ title, prompt, icon: Icon, onClick }) => (
    <motion.button
        onClick={() => onClick(prompt)}
        whileHover={{ scale: 1.02 }}
        whileTap={{ scale: 0.98 }}
        className="group relative w-full h-48 rounded-xl perspective-1000 overflow-hidden text-left"
    >
        {/* Card Background & Gradient */}
        <div className="absolute inset-0 bg-gradient-to-br from-[#1a1a1a] to-black border border-white/5 rounded-xl transition-all duration-500 group-hover:border-gold/30">
            {/* Animated Gold Blur Blob */}
            <div className="absolute -top-10 -right-10 w-32 h-32 bg-gold/10 rounded-full blur-3xl opacity-0 group-hover:opacity-100 transition-opacity duration-700 animate-pulse" />
        </div>

        {/* Content */}
        <div className="relative z-10 p-6 flex flex-col justify-between h-full">
            <div>
                <div className="w-10 h-10 rounded-lg bg-white/5 flex items-center justify-center mb-4 transition-colors group-hover:bg-gold/10">
                    <Icon className="w-5 h-5 text-gray-400 group-hover:text-gold transition-colors" />
                </div>
                <h3 className="font-sovereign text-xl text-gray-200 group-hover:text-white transition-colors">{title}</h3>
            </div>
            <p className="font-sans text-xs text-gray-500 group-hover:text-gray-400 transition-colors pr-4">{prompt}</p>
        </div>
    </motion.button>
);

// Infinite Marquee Component
const InfiniteMarquee = () => {
    const companies = [
        "APPLE", "MICROSOFT", "GOOGLE", "AMAZON", "TESLA", "NVIDIA", "META", "BERKSHIRE", "JPMORGAN"
    ];

    return (
        <div className="relative w-full overflow-hidden border-y border-white/5 bg-black/20 backdrop-blur-sm py-3 mt-12 mb-8">
            <div className="flex animate-scroll whitespace-nowrap">
                {[...companies, ...companies].map((company, i) => (
                    <div key={i} className="flex items-center mx-8">
                        <span className="font-sovereign text-gold text-lg mr-2">✦</span>
                        <span className="font-sans text-[10px] tracking-[0.2em] text-gray-400 uppercase">{company}</span>
                    </div>
                ))}
            </div>
            {/* Gradient Fade Edges */}
            <div className="absolute inset-y-0 left-0 w-24 bg-gradient-to-r from-obsidian to-transparent z-10" />
            <div className="absolute inset-y-0 right-0 w-24 bg-gradient-to-l from-obsidian to-transparent z-10" />
        </div>
    );
};

const ChatInterface = () => {
    const [messages, setMessages] = useState([]);
    const [input, setInput] = useState('');
    const [isLoading, setIsLoading] = useState(false);
    const [isApiKeyModalOpen, setIsApiKeyModalOpen] = useState(false);
    const messagesEndRef = useRef(null);

    const scrollToBottom = () => {
        messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
    };

    useEffect(() => {
        scrollToBottom();
    }, [messages.length]);

    const suggestions = [
        { title: "Analyze Revenue", prompt: "Compare Apple and Microsoft revenue streams for the last fiscal year.", icon: TrendingUp },
        { title: "Risk Assessment", prompt: "Identify the top 3 risk factors from Google's latest 10-K filing.", icon: AlertTriangle },
        { title: "Financial Summary", prompt: "Provide a comprehensive net income summary for Tesla in 2023.", icon: FileText }
    ];

    const handleSend = async (text = input) => {
        if (!text.trim()) return;

        // Check for API Key first
        const apiKey = localStorage.getItem('openai_key');
        if (!apiKey || !apiKey.startsWith('sk-')) {
            setIsApiKeyModalOpen(true);
            return;
        }

        const userMessage = { content: text, sender: 'user', id: Date.now() };

        // Prepare AI placeholder
        const aiMessageId = Date.now() + 1;
        const aiPlaceholder = {
            id: aiMessageId,
            sender: 'ai',
            content: '',
            thinkingSteps: ["Initializing agent..."],
            isThinkingOpen: true,
            isDone: false,
            isChart: false
        };

        setMessages(prev => [...prev, userMessage, aiPlaceholder]);
        setInput('');
        setIsLoading(true);

        const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

        try {
            const response = await fetch(`${API_URL}/chat`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'Authorization': `Bearer ${apiKey}`
                },
                body: JSON.stringify({ query: text })
            });

            if (response.status === 401) {
                // Remove invalid key to trigger modal
                localStorage.removeItem('openai_key');
                setIsApiKeyModalOpen(true);
                // We should probably inform the user why it failed, but the modal opening suggests it.
                // Remove the failed AI message or update it to error?
                // Let's update the AI message to say "Auth failed".
                setMessages(prev => prev.map(msg =>
                    msg.id === aiMessageId
                        ? { ...msg, content: "Authentication failed. Please check your API Key.", isError: true, isDone: true }
                        : msg
                ));
                setIsLoading(false);
                return;
            }

            if (!response.body) throw new Error('No readable stream');

            const reader = response.body.getReader();
            const decoder = new TextDecoder();
            let done = false;

            while (!done) {
                const { value, done: doneReading } = await reader.read();
                done = doneReading;
                const chunkValue = decoder.decode(value);

                // Split by double newline as per standard SSE or just JSON objects
                // Our backend sends `json + "\n\n"`.
                const lines = chunkValue.split('\n\n').filter(Boolean);

                for (const line of lines) {
                    try {
                        const data = JSON.parse(line);

                        setMessages(prev => prev.map(msg => {
                            if (msg.id !== aiMessageId) return msg;

                            if (data.type === 'log') {
                                return {
                                    ...msg,
                                    thinkingSteps: [...msg.thinkingSteps, data.message]
                                };
                            } else if (data.type === 'result') {
                                return {
                                    ...msg,
                                    content: typeof data.data === 'string' ? data.data : data.data,
                                    isChart: typeof data.data === 'object' && data.data.type === 'chart',
                                    isDone: true,
                                    isThinkingOpen: false // Collapse thinking when done
                                };
                            }
                            return msg;
                        }));
                    } catch (e) {
                        console.error("Error parsing chunk", e);
                    }
                }
            }
        } catch (error) {
            console.error("Streaming error:", error);
            setMessages(prev => prev.map(msg => {
                if (msg.id === aiMessageId) {
                    return { ...msg, content: "Error: Could not fetch response. Please check your connection and API Key.", isError: true, isDone: true };
                }
                return msg;
            }));
        } finally {
            setIsLoading(false);
        }
    };

    const toggleThinking = (id) => {
        setMessages(prev => prev.map(msg => {
            if (msg.id === id) {
                return { ...msg, isThinkingOpen: !msg.isThinkingOpen };
            }
            return msg;
        }));
    };

    return (
        <div className="relative w-full h-screen bg-obsidian text-white overflow-hidden font-sans">
            <BackgroundWave />
            <ApiKeyModal isOpen={isApiKeyModalOpen} onClose={() => setIsApiKeyModalOpen(false)} />

            {/* Header - Fixed Top */}
            <header className="fixed top-0 left-0 right-0 z-50 py-6 px-8 flex justify-between items-center pointer-events-none bg-gradient-to-b from-obsidian via-obsidian to-transparent pb-8">
                <div>
                    <h1 className="font-sovereign text-3xl tracking-tight text-white mb-1">Sovereign.</h1>
                    <p className="text-[10px] uppercase tracking-[0.3em] text-gold/80 font-medium ml-1">Financial Intelligence</p>
                </div>
                {messages.length !== 0 && (
                    <div className="pointer-events-auto">
                        <button
                            onClick={() => window.location.reload()}
                            className="text-xs uppercase tracking-[0.15em] text-gold/80 hover:text-gold transition-colors font-medium px-4 py-2 border border-gold/20 hover:border-gold/40 rounded-lg bg-black/20 hover:bg-black/40 backdrop-blur-sm"
                        >
                            New Chat
                        </button>
                    </div>
                )}
            </header>

            {/* Main Chat Area */}
            <main className="relative z-10 w-full h-full pt-24 overflow-y-auto no-scrollbar scroll-smooth">
                {/* Full Width Container for Marquee */}
                <div className="w-full min-h-full flex flex-col">
                    <AnimatePresence mode="popLayout">
                        {messages.length === 0 ? (
                            <motion.div
                                initial={{ opacity: 0, y: 20 }}
                                animate={{ opacity: 1, y: 0 }}
                                exit={{ opacity: 0, y: -20 }}
                                className="flex-1 flex flex-col items-center justify-center min-h-[60vh] pb-8 text-center"
                            >
                                <h2 className="font-sovereign text-5xl md:text-7xl mb-8 text-white leading-tight">
                                    Financial Clarity,<br />
                                    <span className="text-gold italic">Redefined.</span>
                                </h2>

                                <div className="grid grid-cols-1 md:grid-cols-3 gap-6 w-full max-w-4xl px-6 mt-8">
                                    {suggestions.map((s, i) => (
                                        <HolographicCard
                                            key={i}
                                            title={s.title}
                                            prompt={s.prompt}
                                            icon={s.icon}
                                            onClick={handleSend}
                                        />
                                    ))}
                                </div>

                                <InfiniteMarquee />
                            </motion.div>
                        ) : (
                            <div className="max-w-4xl mx-auto px-6 w-full pt-8 pb-48">
                                <div className="space-y-12">
                                    {messages.map((msg) => (
                                        <motion.div
                                            key={msg.id}
                                            initial={{ opacity: 0, y: 10 }}
                                            animate={{ opacity: 1, y: 0 }}
                                            className={`flex gap-8 ${msg.sender === 'user' ? 'justify-end' : 'justify-start'}`}
                                        >
                                            {msg.sender === 'ai' && (
                                                <div className="w-10 h-10 rounded-full border border-gold/40 flex items-center justify-center flex-shrink-0 mt-1 bg-black">
                                                    <span className="font-sovereign text-gold text-lg italic">S</span>
                                                </div>
                                            )}

                                            <div className={`flex flex-col max-w-[85%] md:max-w-[80%] ${msg.sender === 'user' ? 'items-end' : 'items-start'}`}>
                                                {msg.sender === 'user' && (
                                                    <div className="mb-2 text-[10px] uppercase tracking-widest text-gray-500">You</div>
                                                )}

                                                {msg.sender === 'ai' && msg.thinkingSteps && (
                                                    <ThinkingDropdown
                                                        steps={msg.thinkingSteps}
                                                        isOpen={msg.isThinkingOpen}
                                                        setIsOpen={() => toggleThinking(msg.id)}
                                                        isDone={msg.isDone}
                                                    />
                                                )}

                                                {msg.content && (
                                                    msg.isChart ? (
                                                        <div className="w-full bg-obsidian border border-white/10 p-6 shadow-2xl overflow-hidden">
                                                            <FinancialChart data={typeof msg.content === 'string' ? JSON.parse(msg.content) : msg.content} />
                                                        </div>
                                                    ) : (
                                                        <div className={`text-base md:text-lg leading-loose font-light ${msg.sender === 'user'
                                                            ? 'text-white/90 text-right'
                                                            : msg.isError ? 'text-red-400' : 'text-gray-200'
                                                            }`}>
                                                            {msg.sender === 'ai' && !msg.isError ? (
                                                                <div className="prose prose-invert prose-lg max-w-none prose-p:font-light prose-headings:font-sovereign prose-headings:text-white prose-strong:text-gold prose-a:text-gold">
                                                                    <ReactMarkdown remarkPlugins={[remarkGfm]}>
                                                                        {msg.content}
                                                                    </ReactMarkdown>
                                                                </div>
                                                            ) : (
                                                                <p className="whitespace-pre-wrap">{msg.content}</p>
                                                            )}
                                                        </div>
                                                    )
                                                )}
                                            </div>

                                            {msg.sender === 'user' && (
                                                <div className="w-10 h-10 rounded-full border border-white/20 flex items-center justify-center flex-shrink-0 mt-1 bg-white/5">
                                                    <User className="w-4 h-4 text-gray-300" />
                                                </div>
                                            )}
                                        </motion.div>
                                    ))}

                                    {isLoading && messages.length > 0 && messages[messages.length - 1].sender === 'user' && (
                                        <motion.div initial={{ opacity: 0 }} animate={{ opacity: 1 }} className="flex gap-8 justify-start">
                                            <div className="w-10 h-10 rounded-full border border-gold/40 flex items-center justify-center flex-shrink-0 mt-1 bg-black">
                                                <span className="font-sovereign text-gold text-lg italic">S</span>
                                            </div>
                                            <div className="flex flex-col gap-2 pt-2">
                                                <span className="font-sovereign text-gold italic text-lg animate-pulse">Consulting 10-K Filings...</span>
                                                <ThinkingDropdown steps={["Accessing SEC Database..."]} isOpen={true} isDone={false} setIsOpen={() => { }} />
                                            </div>
                                        </motion.div>
                                    )}
                                    <div ref={messagesEndRef} />
                                </div>
                            </div>
                        )}
                    </AnimatePresence>
                </div>
            </main>

            {/* Input Area - Fixed Bottom */}
            <div className="fixed bottom-0 left-0 right-0 z-50 px-4 pb-6 pt-8 pointer-events-none flex justify-center bg-gradient-to-t from-obsidian via-obsidian to-transparent">
                <div className="w-full max-w-3xl pointer-events-auto relative">
                    <form onSubmit={(e) => { e.preventDefault(); handleSend(); }} className="relative group">
                        {/* Glow Effect */}
                        <div className="absolute -inset-1 bg-gradient-to-r from-gold/20 via-white/10 to-gold/20 rounded-full opacity-0 group-hover:opacity-100 blur-xl transition-opacity duration-700" />

                        <div className="relative flex items-center bg-obsidian/80 backdrop-blur-xl border border-white/10 rounded-full shadow-2xl overflow-hidden transition-all duration-300 group-focus-within:border-gold/30">
                            <input
                                type="text"
                                value={input}
                                onChange={(e) => setInput(e.target.value)}
                                placeholder="Inquire about market intelligence..."
                                className="w-full bg-transparent text-white placeholder-gray-500 pl-6 pr-14 py-4 focus:outline-none font-sans font-light text-base tracking-wide"
                            />
                            <div className="absolute right-4 top-1/2 -translate-y-1/2">
                                <Button
                                    type="submit"
                                    disabled={!input.trim() || isLoading}
                                    variant="ghost"
                                    size="icon"
                                    className={`rounded-full w-12 h-12 flex items-center justify-center transition-all duration-500 ${input.trim()
                                        ? 'bg-gold text-obsidian hover:bg-white hover:text-obsidian scale-100'
                                        : 'bg-white/5 text-gray-600'
                                        }`}
                                >
                                    <ArrowUp className="w-5 h-5" />
                                </Button>
                            </div>
                        </div>
                    </form>
                    <div className="mt-4 text-center">
                        <span className="text-[9px] uppercase tracking-[0.25em] text-gray-600 font-medium">Sovereign Intelligence • Beta</span>
                    </div>
                </div>
            </div>
        </div>
    );
};

export default ChatInterface;
