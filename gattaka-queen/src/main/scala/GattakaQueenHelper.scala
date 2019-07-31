package ai.scynet.queen

import akka.actor.ActorRef
import com.obecto.gattakka.PipelineOperator
import com.obecto.gattakka.genetics.Genome
import com.obecto.gattakka.genetics.descriptors.{DoubleGeneDescriptor, MapGeneGroupDescriptor}
import com.obecto.gattakka.genetics.operators._
import com.obecto.gattakka.messages.population.RefreshPopulation

object Definitions {
  val chromosomeDescriptor = MapGeneGroupDescriptor(
    "x" -> DoubleGeneDescriptor(-100, 100),
    "y" -> DoubleGeneDescriptor(-100, 100),
  )
}

class GattakaQueenHelper {
  def evaluator = classOf[QueenEvaluator]

  def individualActor = classOf[CustomIndividualActor]

  def refreshPopulation(actor: ActorRef): Unit = {
    actor ! RefreshPopulation()
  }

  val initialChromosomes = (1 to 50).map((i: Int) => {
    Genome(List(
      Definitions.chromosomeDescriptor.createChromosome()
    ))
  }).toList

  val pipelineOperators: List[PipelineOperator] = List(
    new EliteOperator {
      val elitePercentage = 0.1
    },
    new UniformCrossoverReplicationOperator {
      val replicationChance = 0.5
      override val keepFirstChildOnly = true
      // val parentSelectionStrategy = new RouletteWheelSelectionStrategy()
      val parentSelectionStrategy = new TournamentSelectionStrategy(4)
      // val parentSelectionStrategy = new TournamentSelectionStrategy(1)
    },
    new BinaryMutationOperator {
      val mutationChance = 0.2
      val bitFlipChance = 2.0 / 16
    },
    new DeduplicationOperator {},
    new DiversitySelectionOperator {
      val targetPopulationSize = 50
    },
  )
}
