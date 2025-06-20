import React from 'react';
import { motion } from 'framer-motion';
import Lottie from 'lottie-react';
import { 
  Brain, 
  MessageSquare, 
  BarChart3, 
  Shield, 
  Clock, 
  Workflow,
  Zap,
  Users,
  Settings
} from 'lucide-react';

const Features = () => {
  const features = [
    {
      icon: Brain,
      title: 'Advanced AI Intelligence',
      description: 'Powered by cutting-edge machine learning algorithms that adapt and learn from your business patterns.',
      color: 'from-purple-500 to-pink-500'
    },
    {
      icon: MessageSquare,
      title: 'Natural Language Processing',
      description: 'Communicate with your AI agents using natural language. No coding or complex commands required.',
      color: 'from-blue-500 to-cyan-500'
    },
    {
      icon: Workflow,
      title: 'Automated Workflows',
      description: 'Create complex automation workflows that handle repetitive tasks and scale with your business.',
      color: 'from-green-500 to-emerald-500'
    },
    {
      icon: BarChart3,
      title: 'Real-time Analytics',
      description: 'Get detailed insights into your automation performance with comprehensive analytics and reporting.',
      color: 'from-orange-500 to-red-500'
    },
    {
      icon: Shield,
      title: 'Enterprise Security',
      description: 'Bank-level security with end-to-end encryption and compliance with major industry standards.',
      color: 'from-indigo-500 to-purple-500'
    },
    {
      icon: Clock,
      title: '24/7 Operation',
      description: 'Your AI agents work around the clock, handling tasks even when your team is offline.',
      color: 'from-teal-500 to-blue-500'
    }
  ];

  const demoFeatures = [
    {
      icon: Zap,
      title: 'Lightning Fast Setup',
      description: 'Get started in minutes with our intuitive setup wizard.'
    },
    {
      icon: Users,
      title: 'Team Collaboration',
      description: 'Work together seamlessly with built-in collaboration tools.'
    },
    {
      icon: Settings,
      title: 'Custom Integrations',
      description: 'Connect with your existing tools and platforms effortlessly.'
    }
  ];

  // Simple Lottie animation for workflow
  const workflowAnimation = {
    "v": "5.7.4",
    "fr": 30,
    "ip": 0,
    "op": 60,
    "w": 200,
    "h": 200,
    "nm": "Workflow",
    "ddd": 0,
    "assets": [],
    "layers": [
      {
        "ddd": 0,
        "ind": 1,
        "ty": 4,
        "nm": "Arrow",
        "sr": 1,
        "ks": {
          "o": {"a": 0, "k": 100},
          "r": {"a": 0, "k": 0},
          "p": {"a": 1, "k": [
            {"i": {"x": 0.833, "y": 0.833}, "o": {"x": 0.167, "y": 0.167}, "t": 0, "s": [50, 100, 0]},
            {"i": {"x": 0.833, "y": 0.833}, "o": {"x": 0.167, "y": 0.167}, "t": 30, "s": [150, 100, 0]},
            {"t": 60, "s": [50, 100, 0]}
          ]},
          "a": {"a": 0, "k": [0, 0, 0]},
          "s": {"a": 0, "k": [100, 100, 100]}
        },
        "ao": 0,
        "shapes": [
          {
            "ty": "gr",
            "it": [
              {
                "ind": 0,
                "ty": "sh",
                "ks": {
                  "a": 0,
                  "k": {
                    "i": [[0, 0], [0, 0], [0, 0]],
                    "o": [[0, 0], [0, 0], [0, 0]],
                    "v": [[-20, 0], [20, 0], [10, -10]],
                    "c": false
                  }
                },
                "nm": "Path 1",
                "mn": "ADBE Vector Shape - Group"
              },
              {
                "ty": "st",
                "c": {"a": 0, "k": [0.3, 0.7, 1, 1]},
                "o": {"a": 0, "k": 100},
                "w": {"a": 0, "k": 4},
                "lc": 2,
                "lj": 2,
                "bm": 0,
                "nm": "Stroke 1",
                "mn": "ADBE Vector Graphic - Stroke"
              }
            ],
            "nm": "Arrow",
            "np": 2,
            "cix": 2,
            "bm": 0,
            "ix": 1,
            "mn": "ADBE Vector Group"
          }
        ],
        "ip": 0,
        "op": 60,
        "st": 0,
        "bm": 0
      }
    ]
  };

  return (
    <section id="features" className="py-24 bg-gray-50">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: false }}
          transition={{ duration: 0.6 }}
          className="text-center mb-20"
        >
          <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
            Powerful Features for
            <span className="bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent">
              {' '}Modern Business
            </span>
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Discover how our AI agents can transform your business operations with 
            intelligent automation and seamless integration.
          </p>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8 mb-20">
          {features.map((feature, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: false }}
              transition={{ duration: 0.6, delay: index * 0.1 }}
              whileHover={{ y: -5, scale: 1.02 }}
              className="bg-white rounded-2xl p-8 shadow-lg hover:shadow-xl transition-all duration-300"
            >
              <motion.div
                initial={{ scale: 0 }}
                whileInView={{ scale: 1 }}
                viewport={{ once: false }}
                transition={{ duration: 0.5, delay: index * 0.1 + 0.2 }}
                whileHover={{ rotate: 5 }}
                className={`w-16 h-16 rounded-2xl bg-gradient-to-r ${feature.color} flex items-center justify-center mb-6`}
              >
                <feature.icon className="h-8 w-8 text-white" />
              </motion.div>
              <h3 className="text-xl font-semibold text-gray-900 mb-4">
                {feature.title}
              </h3>
              <p className="text-gray-600 leading-relaxed">
                {feature.description}
              </p>
            </motion.div>
          ))}
        </div>

        {/* Demo Section with Lottie */}
        <motion.div
          initial={{ opacity: 0, y: 40 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: false }}
          transition={{ duration: 0.8 }}
          className="bg-gradient-to-r from-purple-900 to-blue-900 rounded-3xl p-8 md:p-12 text-white"
        >
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-12 items-center">
            <div>
              <div className="text-center lg:text-left mb-8">
                <h3 className="text-3xl md:text-4xl font-bold mb-4">
                  See AgentFlow in Action
                </h3>
                <p className="text-xl text-purple-200 max-w-2xl">
                  Watch how our AI agents can streamline your workflows and boost productivity
                </p>
              </div>

              <div className="grid grid-cols-1 gap-6 mb-8">
                {demoFeatures.map((feature, index) => (
                  <motion.div
                    key={index}
                    initial={{ opacity: 0, x: -20 }}
                    whileInView={{ opacity: 1, x: 0 }}
                    viewport={{ once: false }}
                    transition={{ duration: 0.6, delay: index * 0.2 }}
                    className="flex items-center space-x-4"
                  >
                    <motion.div
                      whileHover={{ scale: 1.1, rotate: 5 }}
                      className="w-12 h-12 bg-white/10 rounded-xl flex items-center justify-center flex-shrink-0"
                    >
                      <feature.icon className="h-6 w-6 text-cyan-400" />
                    </motion.div>
                    <div>
                      <h4 className="text-lg font-semibold mb-1">{feature.title}</h4>
                      <p className="text-purple-200 text-sm">{feature.description}</p>
                    </div>
                  </motion.div>
                ))}
              </div>

              <motion.div
                initial={{ opacity: 0, scale: 0.9 }}
                whileInView={{ opacity: 1, scale: 1 }}
                viewport={{ once: false }}
                transition={{ duration: 0.6, delay: 0.4 }}
              >
                <motion.button
                  whileHover={{ scale: 1.05 }}
                  whileTap={{ scale: 0.95 }}
                  className="bg-white text-purple-900 px-8 py-4 rounded-full text-lg font-semibold hover:shadow-lg transition-all duration-300"
                >
                  Request Demo
                </motion.button>
              </motion.div>
            </div>

            {/* Lottie Animation */}
            <motion.div
              initial={{ opacity: 0, scale: 0.8 }}
              whileInView={{ opacity: 1, scale: 1 }}
              viewport={{ once: false }}
              transition={{ duration: 0.8, delay: 0.3 }}
              className="flex justify-center"
            >
              <div className="relative">
                <motion.div
                  animate={{ rotate: 360 }}
                  transition={{ duration: 20, repeat: Infinity, ease: "linear" }}
                  className="w-80 h-80 bg-white/10 rounded-full flex items-center justify-center backdrop-blur-sm border border-white/20"
                >
                  <motion.div
                    animate={{ rotate: -360 }}
                    transition={{ duration: 15, repeat: Infinity, ease: "linear" }}
                    className="w-60 h-60 bg-gradient-to-r from-cyan-400/20 to-purple-400/20 rounded-full flex items-center justify-center"
                  >
                    <Lottie 
                      animationData={workflowAnimation}
                      loop={true}
                      className="w-40 h-40"
                    />
                  </motion.div>
                </motion.div>
                
                {/* Floating workflow icons */}
                <motion.div
                  animate={{ 
                    y: [0, -15, 0],
                    rotate: [0, 10, 0]
                  }}
                  transition={{ 
                    duration: 3, 
                    repeat: Infinity, 
                    ease: "easeInOut" 
                  }}
                  className="absolute -top-4 -right-4 w-16 h-16 bg-cyan-400/20 rounded-full flex items-center justify-center backdrop-blur-sm border border-cyan-400/30"
                >
                  <Workflow className="h-8 w-8 text-cyan-400" />
                </motion.div>
                
                <motion.div
                  animate={{ 
                    y: [0, 15, 0],
                    rotate: [0, -10, 0]
                  }}
                  transition={{ 
                    duration: 4, 
                    repeat: Infinity, 
                    ease: "easeInOut",
                    delay: 1
                  }}
                  className="absolute -bottom-4 -left-4 w-16 h-16 bg-purple-400/20 rounded-full flex items-center justify-center backdrop-blur-sm border border-purple-400/30"
                >
                  <Brain className="h-8 w-8 text-purple-400" />
                </motion.div>
              </div>
            </motion.div>
          </div>
        </motion.div>
      </div>
    </section>
  );
};

export default Features;