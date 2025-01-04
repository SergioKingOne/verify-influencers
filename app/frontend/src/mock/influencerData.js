export const mockInfluencerData = {
  username: "hubermanlab",
  profile_image:
    "https://pbs.twimg.com/profile_images/1339713932085346306/jDTi4HKH_400x400.jpg",
  follower_count: 4200000,
  tweets: [
    "New research shows that viewing sunlight within 30-50 minutes of waking enhances cortisol release and improves energy levels throughout the day.",
    "NSDR (Non-Sleep Deep Rest) protocols can accelerate learning and recovery. Just 10-20 minutes can reset your nervous system.",
    "Cold exposure of 11C/52F for 1-5 minutes increases dopamine by 250% and norepinephrine by 530% for up to an hour",
  ],
  health_claims: [
    "Viewing sunlight within 30-50 minutes of waking enhances cortisol release",
    "Non-sleep deep rest (NSDR) protocols can accelerate learning and recovery",
    "Cold exposure increases dopamine and norepinephrine levels",
  ],
  verification_results: {
    "Viewing sunlight within 30-50 minutes of waking enhances cortisol release":
      {
        verification_status: "Verified",
        supporting_evidence: [
          "Multiple studies have demonstrated that morning light exposure significantly affects cortisol awakening response (CAR) and circadian rhythm entrainment.",
          "Research indicates optimal timing window of 30-60 minutes post-wake for maximum benefit.",
        ],
        contradicting_evidence: [],
        trust_score: 92,
      },
    "Non-sleep deep rest (NSDR) protocols can accelerate learning and recovery":
      {
        verification_status: "Verified",
        supporting_evidence: [
          "Studies on yoga nidra and meditation show enhanced recovery and learning consolidation.",
          "Neuroimaging reveals increased neural plasticity during restful alert states.",
        ],
        contradicting_evidence: [],
        trust_score: 88,
      },
    "Cold exposure increases dopamine and norepinephrine levels": {
      verification_status: "Questionable",
      supporting_evidence: [
        "Some evidence supports acute catecholamine response to cold exposure.",
      ],
      contradicting_evidence: [
        "Exact temperature and duration requirements need more research.",
        "Long-term effects are not well established.",
      ],
      trust_score: 75,
    },
  },
  stats: {
    trust_score: 89,
    yearly_revenue: "5.0M",
    products_count: 1,
    total_claims_analyzed: 127,
  },
  categories: [
    "Sleep",
    "Performance",
    "Hormones",
    "Nutrition",
    "Exercise",
    "Stress",
    "Cognition",
  ],
};
