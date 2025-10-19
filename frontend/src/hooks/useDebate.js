import { useState, useCallback } from 'react';

export const useDebate = (topic) => {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [debateActive, setDebateActive] = useState(false);
  const [score, setScore] = useState({ human: 0, ai: 0 });
  const [loading, setLoading] = useState(false);
  const [uploadedDocs, setUploadedDocs] = useState([]);
  const [currentAgent, setCurrentAgent] = useState('');
  const [roundNumber, setRoundNumber] = useState(0);
  const [debateHistory, setDebateHistory] = useState([]);

  // Simulated agents
  const agents = {
    keywordExtractor: (text) => {
      const words = text.toLowerCase().split(/\W+/);
      const stopWords = ['the', 'is', 'at', 'which', 'on', 'a', 'an', 'and', 'or', 'but', 'we', 'to', 'that'];
      return words.filter(w => w.length > 4 && !stopWords.includes(w)).slice(0, 5);
    },

    counterArgumentGenerator: (argument, topic, keywords, previousContext = []) => {
      const topicLower = topic.toLowerCase();
      const roundCount = previousContext.length;

      if (topicLower.includes('climate') && topicLower.includes('immediate')) {
        if (roundCount === 0) {
          return `While climate change is a concern, immediate drastic action could cause severe economic disruption. Developing nations need time to transition their economies, and forcing rapid changes could push millions into poverty. Countries like China and India need fossil fuels to lift their populations out of poverty - immediate action would disproportionately harm the world's poorest. Historical data shows technological innovation, not emergency policy, has solved past environmental challenges.`;
        } else if (roundCount === 1) {
          return `The "cost of inaction" argument uses inflated projections from worst-case scenarios that assume zero adaptation. The Netherlands has lived below sea level for centuries through engineering - humans adapt remarkably well. Germany's Energiewende cost €500 billion yet increased emissions when they closed nuclear plants. Rapid transitions have consistently failed.`;
        } else {
          return `After ${roundCount + 1} rounds, the fundamental contradiction in your position remains: you demand immediate global action while enforcement mechanisms don't exist and developing nations won't comply. Your moral arguments about future generations ignore the moral obligation to current generations struggling with poverty.`;
        }
      }

      if (roundCount === 0) {
        return `However, this perspective overlooks critical economic and practical realities. The proposed approach would require massive resource reallocation that many communities cannot afford. Historical precedents show gradual, market-driven transitions are more sustainable than forced immediate changes.`;
      } else {
        return `In round ${roundCount + 1}, you still haven't addressed the fundamental flaws in your position. The examples I've cited demonstrate that your approach doesn't work in practice. We need solutions that work in the real world, not theories that sound good in academic papers.`;
      }
    },

    evaluationAgent: (humanArg, aiArg) => {
      const humanScore = Math.min(
        3 +
          (humanArg.length > 100 ? 2 : 0) +
          (humanArg.match(/evidence|research|study|data|specific|example/gi) || []).length * 0.5 +
          (humanArg.match(/\d+/g) || []).length * 0.5,
        10
      );

      const aiScore = Math.min(
        3 +
          (aiArg.length > 100 ? 2 : 0) +
          (aiArg.match(/evidence|research|study|data|specific|example/gi) || []).length * 0.5 +
          (aiArg.match(/\d+/g) || []).length * 0.5,
        10
      );

      return {
        humanScore: Math.round(humanScore),
        aiScore: Math.round(aiScore),
        feedback:
          humanScore > aiScore
            ? 'Strong argument with good evidence and reasoning'
            : 'AI presented more comprehensive reasoning with specific examples'
      };
    }
  };

  const startDebate = useCallback(
    (debateTopic) => {
      if (!debateTopic.trim()) {
        alert('Please enter a debate topic first');
        return;
      }
      setDebateActive(true);
      setMessages([
        {
          type: 'system',
          content: `Debate started on topic: "${debateTopic}". Present your opening argument. This will be a multi-round debate.`,
          timestamp: new Date().toLocaleTimeString()
        }
      ]);
      setScore({ human: 0, ai: 0 });
      setCurrentAgent('');
      setRoundNumber(0);
      setDebateHistory([]);
    },
    []
  );

  const handleSendMessage = useCallback(() => {
    if (!input.trim() || !debateActive) return;

    const currentRound = roundNumber + 1;
    const userMessage = {
      type: 'human',
      content: input,
      timestamp: new Date().toLocaleTimeString(),
      round: currentRound
    };

    setMessages(prev => [...prev, userMessage]);
    const currentInput = input;
    setInput('');
    setLoading(true);

    setTimeout(() => {
      setCurrentAgent('Keyword Extractor');

      setTimeout(() => {
        const keywords = agents.keywordExtractor(currentInput);
        setCurrentAgent('Counter-Argument Generator');

        setTimeout(() => {
          const counterArg = agents.counterArgumentGenerator(currentInput, topic, keywords, debateHistory);
          setCurrentAgent('Evaluation Agent');

          setTimeout(() => {
            const evaluation = agents.evaluationAgent(currentInput, counterArg);

            setMessages(prev => [
              ...prev,
              {
                type: 'ai',
                content: counterArg,
                timestamp: new Date().toLocaleTimeString(),
                keywords: keywords,
                round: currentRound
              },
              {
                type: 'evaluation',
                content: `Round ${currentRound} Score - Human: ${evaluation.humanScore}/10, AI: ${evaluation.aiScore}/10. ${evaluation.feedback}`,
                timestamp: new Date().toLocaleTimeString(),
                round: currentRound
              }
            ]);

            setScore(prev => ({
              human: prev.human + evaluation.humanScore,
              ai: prev.ai + evaluation.aiScore
            }));

            setDebateHistory(prev => [
              ...prev,
              {
                round: currentRound,
                human: currentInput,
                ai: counterArg
              }
            ]);

            setRoundNumber(currentRound);
            setCurrentAgent('');
            setLoading(false);
          }, 1200);
        }, 1200);
      }, 800);
    }, 500);
  }, [input, debateActive, topic, roundNumber, debateHistory, agents]);

  const handleAdmitDefeat = useCallback(
    (winner) => {
      setMessages(prev => [
        ...prev,
        {
          type: 'system',
          content: `${winner === 'ai' ? 'Human' : 'AI'} admits defeat! ${winner === 'ai' ? 'AI' : 'Human'} wins the debate!`,
          timestamp: new Date().toLocaleTimeString()
        }
      ]);
      setDebateActive(false);
    },
    []
  );

  const handleFileUpload = useCallback((e) => {
    const files = Array.from(e.target.files);
    setUploadedDocs(prev => [...prev, ...files.map(f => f.name)]);
    setMessages(prev => [
      ...prev,
      {
        type: 'system',
        content: `Uploaded documents: ${files.map(f => f.name).join(', ')}. Knowledge base updated.`,
        timestamp: new Date().toLocaleTimeString()
      }
    ]);
  }, []);

  const simulateWebScrape = useCallback((topic) => {
    setMessages(prev => [
      ...prev,
      {
        type: 'system',
        content: `Web scraping initiated for topic: "${topic}". Retrieved 15 articles from credible sources.`,
        timestamp: new Date().toLocaleTimeString()
      }
    ]);
  }, []);

  return {
    messages,
    input,
    setInput,
    debateActive,
    score,
    loading,
    roundNumber,
    currentAgent,
    uploadedDocs,
    startDebate,
    handleSendMessage,
    handleAdmitDefeat,
    handleFileUpload,
    simulateWebScrape
  };
};