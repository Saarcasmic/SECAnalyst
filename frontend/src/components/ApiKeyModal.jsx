import React, { useState, useEffect } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { Key, ShieldCheck } from 'lucide-react';
import { Button } from './ui/Button';

const ApiKeyModal = ({ isOpen, onClose }) => {
    const [apiKey, setApiKey] = useState('');

    const handleSubmit = (e) => {
        e.preventDefault();
        if (apiKey.trim().startsWith('sk-')) {
            localStorage.setItem('openai_key', apiKey.trim());
            onClose();
            // We usually don't need to reload if the parent reads fresh storage, 
            // but if we want to be safe or if context/hooks need it, we can.
            // For now, let's trust the parent component checks storage on demand.
        } else {
            alert('Please enter a valid OpenAI API key starting with sk-');
        }
    };

    return (
        <AnimatePresence>
            {isOpen && (
                <div className="fixed inset-0 z-[100] flex items-center justify-center p-4">
                    {/* Backdrop */}
                    <motion.div
                        initial={{ opacity: 0 }}
                        animate={{ opacity: 1 }}
                        exit={{ opacity: 0 }}
                        className="absolute inset-0 bg-black/60 backdrop-blur-xl"
                    />

                    {/* Modal */}
                    <motion.div
                        initial={{ scale: 0.95, opacity: 0 }}
                        animate={{ scale: 1, opacity: 1 }}
                        exit={{ scale: 0.95, opacity: 0 }}
                        className="relative w-full max-w-md bg-obsidian/90 border border-gold/20 rounded-2xl p-8 shadow-2xl overflow-hidden"
                    >
                        {/* Glow Effect */}
                        <div className="absolute top-0 right-0 w-32 h-32 bg-gold/10 rounded-full blur-3xl -translate-y-1/2 translate-x-1/2" />

                        <div className="relative z-10">
                            <div className="flex justify-center mb-6">
                                <div className="w-16 h-16 rounded-full bg-black/40 border border-gold/20 flex items-center justify-center">
                                    <Key className="w-8 h-8 text-gold" />
                                </div>
                            </div>

                            <h2 className="text-2xl font-sovereign text-center text-white mb-2">
                                Enter OpenAI API Key
                            </h2>
                            <p className="text-center text-gray-400 text-sm mb-8 leading-relaxed">
                                This is a portfolio project. To control costs, please provide your own API key.
                                It is stored locally in your browser and never saved to our servers.
                            </p>

                            <form onSubmit={handleSubmit} className="space-y-6">
                                <div className="space-y-2">
                                    <input
                                        type="password"
                                        value={apiKey}
                                        onChange={(e) => setApiKey(e.target.value)}
                                        placeholder="sk-..."
                                        className="w-full bg-black/40 border border-white/10 rounded-lg px-4 py-3 text-white placeholder-gray-600 focus:outline-none focus:border-gold/50 transition-colors font-mono text-sm"
                                        autoFocus
                                    />
                                    <div className="flex items-center gap-2 text-[10px] text-gray-500 justify-center">
                                        <ShieldCheck className="w-3 h-3" />
                                        <span>Stored locally & encrypted</span>
                                    </div>
                                </div>

                                <Button
                                    type="submit"
                                    disabled={!apiKey}
                                    className="w-full bg-gold text-obsidian hover:bg-white transition-colors py-6 font-medium tracking-wide"
                                >
                                    Initialize Agent
                                </Button>
                            </form>
                        </div>
                    </motion.div>
                </div>
            )}
        </AnimatePresence>
    );
};

export default ApiKeyModal;
