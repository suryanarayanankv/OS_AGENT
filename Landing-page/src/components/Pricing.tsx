import React from 'react';
import { motion } from 'framer-motion';
import { Check, ArrowRight, Star, Zap } from 'lucide-react';

const Pricing = () => {
  const plans = [
    {
      name: 'Starter',
      price: '₹2000',
      period: 'per month',
      description: 'Perfect for individuals getting started with AI automation',
      features: [
        '1,000 monthly tasks',
        'Basic integrations',
        '50+ inbuilt tools',
        'LLM of Your Choice',
      ],
      popular: false,
      color: 'from-gray-600 to-gray-700'
    },
    {
      name: 'Professional',
      price: '₹25000',
      period: 'per month',
      description: 'Ideal for growing businesses that need advanced automation',
      features: [
        'Up to 250+ inbuilt tools',
        '10,000 monthly tasks',
        'Advanced integrations',
        'Priority support',
        'Deploy Agent Swarms',
        'Custom workflows',
        'Team collaboration',
        'LLM of Your Choice'],
      popular: true,
      color: 'from-purple-600 to-blue-600'
    },
    {
      name: 'Enterprise',
      price: '₹50000',
      period: 'per month',
      description: 'For large organizations requiring enterprise-grade solutions',
      features: [
        'Up to 250+ inbuilt tools',
        '10,000 monthly tasks',
        'Advanced integrations',
        'Priority support',
        'Deploy Agent Swarms',
        'Custom workflows',
        'Team collaboration',
        'LLM of Your Choice',
        'Custom integrations',
        '24/7 phone support',
        'Advanced security',
        'On-premise deployment'
      ],
      popular: false,
      color: 'from-emerald-600 to-teal-600'
    }
  ];

  return (
    <section id="pricing" className="py-24 bg-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: false }}
          transition={{ duration: 0.6 }}
          className="text-center mb-20"
        >
          <motion.div
            initial={{ scale: 0 }}
            whileInView={{ scale: 1 }}
            viewport={{ once: false }}
            transition={{ duration: 0.5, delay: 0.2 }}
            className="inline-flex items-center space-x-2 bg-purple-100 rounded-full px-6 py-3 mb-6"
          >
            <Star className="h-5 w-5 text-purple-600" />
            <span className="text-purple-700 text-sm font-medium">
              Simple, Transparent Pricing
            </span>
          </motion.div>
          
          <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-6">
            Choose Your
            <span className="bg-gradient-to-r from-purple-600 to-blue-600 bg-clip-text text-transparent">
              {' '}Perfect Plan
            </span>
          </h2>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Start with a free trial and scale as your business grows. No hidden fees, 
            cancel anytime.
          </p>
        </motion.div>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-8 mb-16">
          {plans.map((plan, index) => (
            <motion.div
              key={index}
              initial={{ opacity: 0, y: 30 }}
              whileInView={{ opacity: 1, y: 0 }}
              viewport={{ once: false }}
              transition={{ duration: 0.6, delay: index * 0.1 }}
              whileHover={{ y: -10, scale: 1.02 }}
              className={`relative bg-white rounded-3xl p-8 shadow-lg border-2 transition-all duration-300 ${
                plan.popular 
                  ? 'border-purple-200 shadow-purple-100 shadow-2xl' 
                  : 'border-gray-100 hover:border-purple-100 hover:shadow-xl'
              }`}
            >
              {plan.popular && (
                <motion.div
                  initial={{ scale: 0, rotate: -10 }}
                  whileInView={{ scale: 1, rotate: 0 }}
                  viewport={{ once: false }}
                  transition={{ duration: 0.5, delay: 0.3 }}
                  className="absolute -top-4 left-1/2 transform -translate-x-1/2"
                >
                  <div className="bg-gradient-to-r from-purple-600 to-blue-600 text-white px-6 py-2 rounded-full text-sm font-semibold flex items-center space-x-1">
                    <Zap className="h-4 w-4" />
                    <span>Most Popular</span>
                  </div>
                </motion.div>
              )}

              <div className="text-center mb-8">
                <h3 className="text-2xl font-bold text-gray-900 mb-2">{plan.name}</h3>
                <p className="text-gray-600 mb-6">{plan.description}</p>
                <div className="mb-6">
                  <span className="text-5xl font-bold text-gray-900">{plan.price}</span>
                  <span className="text-gray-500 ml-2">{plan.period}</span>
                </div>
              </div>

              <ul className="space-y-4 mb-8">
                {plan.features.map((feature, featureIndex) => (
                  <motion.li
                    key={featureIndex}
                    initial={{ opacity: 0, x: -20 }}
                    whileInView={{ opacity: 1, x: 0 }}
                    viewport={{ once: false }}
                    transition={{ duration: 0.4, delay: index * 0.1 + featureIndex * 0.1 }}
                    className="flex items-center space-x-3"
                  >
                    <div className="flex-shrink-0 w-5 h-5 bg-green-100 rounded-full flex items-center justify-center">
                      <Check className="h-3 w-3 text-green-600" />
                    </div>
                    <span className="text-gray-700">{feature}</span>
                  </motion.li>
                ))}
              </ul>

              <motion.button
                whileHover={{ scale: 1.05 }}
                whileTap={{ scale: 0.95 }}
                className={`w-full py-4 px-6 rounded-2xl font-semibold flex items-center justify-center space-x-2 transition-all duration-300 ${
                  plan.popular
                    ? 'bg-gradient-to-r from-purple-600 to-blue-600 text-white shadow-lg hover:shadow-xl'
                    : 'bg-gray-900 text-white hover:bg-gray-800'
                }`}
              >
                <span>Get Started</span>
                <ArrowRight className="h-5 w-5" />
              </motion.button>
            </motion.div>
          ))}
        </div>

        <motion.div
          initial={{ opacity: 0, y: 20 }}
          whileInView={{ opacity: 1, y: 0 }}
          viewport={{ once: false }}
          transition={{ duration: 0.6, delay: 0.4 }}
          className="text-center"
        >
          <p className="text-gray-600 mb-6">
            Need a custom solution? We offer enterprise packages tailored to your specific needs.
          </p>
          <motion.button
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.95 }}
            className="bg-gray-100 text-gray-900 px-8 py-3 rounded-full font-semibold hover:bg-gray-200 transition-colors"
          >
            Contact Sales
          </motion.button>
        </motion.div>
      </div>
    </section>
  );
};

export default Pricing;